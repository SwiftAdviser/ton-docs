# Sending messages

Composition, parsing, and sending messages lie at the intersection of [TL-B schemas](/learn/overviews/TL-B), [transaction phases and TVM](/learn/tvm-instructions/tvm-overview.md).

Indeed, FunC exposes [send_raw_message](/develop/func/stdlib#send_raw_message) function which expects a serialized message as an argument.

Since TON is a comprehensive system with wide functionality, messages which need to be able to support all of this functionality may look quite complicated. Still, most of that functionality is not used in common scenarios, and message serialization in most cases may be reduced to:
```func
  cell msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(amount)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
    .store_slice(message_body)
  .end_cell();
```

Therefore, the developer should not be afraid, and if something in this document seems incomprehensible on first reading, it's okay. Just grasp the general idea.

Let's dive in!

## Types of messages
There are three types of messages:
 * external—messages that are sent from outside of the blockchain to a smart contract inside the blockchain. Such messages should be explicitly accepted by smart contracts during so called `credit_gas`. If the message is not accepted, the node should not accept it into a block or relay it to other nodes.
 * internal—messages that are sent from one blockchain entity to another. Such messages (in contrast to external) may carry some TON and pay for themselves. Thus, smart contracts that receive such messages may not accept it. In this case, gas will be deducted from the message value.
 * logs—messages that are sent from a blockchain entity to the outer world. Generally speaking, there is no mechanism for sending such messages out of the blockchain. In fact, while all nodes in the network have consensus on whether a message was created or not, there are no rules on how to process them. Logs may be directly sent to `/dev/null`, logged to disk, saved an indexed database, or even sent by non-blockchain means (email/telegram/sms), all of these are at the sole discretion of the given node.

## Message layout

We will start with the internal message layout.

TL-B scheme, which describes messages that can be sent by smart contracts, is as follows:
```tlb
message$_ {X:Type} info:CommonMsgInfoRelaxed 
  init:(Maybe (Either StateInit ^StateInit))
  body:(Either X ^X) = MessageRelaxed X;
```

Let's put it into words. Serialization of any message consists of three fields: info (header of some sort which describes the source, destination, and other metadata), init (field which is only required for initialization of messages), and body (message payload).

`Maybe` and `Either` and other types of expressions mean the following: 
* when we have the field `info:CommonMsgInfoRelaxed`, it means that the serialization of `CommonMsgInfoRelaxed` is injected directly to the serialization cell.
* when we have the field `body:(Either X ^X)`, it means that when we (de)serialize some type `X`, we first put one `either` bit, which is `0` if `X` is serialized to the same cell, or `1` if it is serialized to the separate cell.
* when we have the field `init:(Maybe (Either StateInit ^StateInit))`, it means that we first put `0` or `1` depending on whether this field is empty or not; and if it is not empty, we serialize `Either StateInit ^StateInit` (again, put one `either` bit which is `0` if `StateInit` is serialized to the same cell or `1` if it is serialized to a separate cell).

`CommonMsgInfoRelaxed` layout is as follows: 

```tlb
int_msg_info$0 ihr_disabled:Bool bounce:Bool bounced:Bool
  src:MsgAddress dest:MsgAddressInt 
  value:CurrencyCollection ihr_fee:Grams fwd_fee:Grams
  created_lt:uint64 created_at:uint32 = CommonMsgInfoRelaxed;

ext_out_msg_info$11 src:MsgAddress dest:MsgAddressExt
  created_lt:uint64 created_at:uint32 = CommonMsgInfoRelaxed;
```

Let's focus on `int_msg_info` for now.
It starts with 1bit prefix `0`, then there are three 1-bit flags, namely whether Instant Hypercube Routing disabled (currently always true), whether message should be bounced if there are errors during it's processing, whether message itself is result of bounce. Then source and destination addresss are serialized, followed by the value of the message and four integers related to message forwarding fees and time.

If a message is sent from the smart contract, some of those fields will be rewritten to the correct values. In particular, validator will rewrite `bounced`, `src`, `ihr_fee`, `fwd_fee`, `created_lt` and `created_at`. That means two things: first, another smart-contract during handling message may trust those fields (sender may not forge source address, `bounced` flag, etc); and second, that during serialization we may put to those fields any valid values (anyway those values will be overwritten).


Straight-forward serialization of the message would be as follows:
```func
  var msg = begin_cell()
    .store_uint(0, 1) ;; tag
    .store_uint(1, 1) ;; ihr_disabled
    .store_uint(1, 1) ;; allow bounces
    .store_uint(0, 1) ;; not bounced itself
    .store_slice(source)
    .store_slice(destination)
    ;; serialize CurrencyCollection (see below)
    .store_coins(amount)
    .store_dict(extra_currencies)
    .store_coins(0) ;; ihr_fee
    .store_coins(fwd_value) ;; fwd_fee 
    .store_uint(cur_lt(), 64) ;; lt of transaction
    .store_uint(now(), 32) ;; unixtime of transaction
    .store_uint(0,  1) ;; no init-field flag (Maybe)
    .store_uint(0,  1) ;; inplace message body flag (Either)
    .store_slice(msg_body)
  .end_cell();
```

However, instead of step-by-step serialization of all fields, usually developers use shortcuts. Thus, let's consider how messages can be sent from the smart contract using an example from [elector-code](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/elector-code.fc#L153).
```func
() send_message_back(addr, ans_tag, query_id, body, grams, mode) impure inline_ref {
  ;; int_msg_info$0 ihr_disabled:Bool bounce:Bool bounced:Bool src:MsgAddress -> 011000
  var msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(grams)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
    .store_uint(ans_tag, 32)
    .store_uint(query_id, 64);
  if (body >= 0) {
    msg~store_uint(body, 32);
  }
  send_raw_message(msg.end_cell(), mode);
}
```

First, it put `0x18` value into 6 bits that is put `0b011000`. What is it? 

* First bit is `0`—1bit prefix which indicates that it is `int_msg_info`. 

* Then there are 3 bits `1`, `1` and `0`, meaning Instant Hypercube Routing is disabled, messages can be bounced, and that message is not the result of bouncing itself. 
* Then there should be sender address, however since it anyway will be rewritten with the same effect any valid address may be stored there. The shortest valid address serialization is that of `addr_none` and it serializes as a two-bit string `00`.

Thus, `.store_uint(0x18, 6)` is the optimized way of serializing the tag and the first 4 fields.

Next line serializes the destination address.

Then we should serialize values. Generally, the message value is a `CurrencyCollection` object with the following scheme:
```tlb
nanograms$_ amount:(VarUInteger 16) = Grams;

extra_currencies$_ dict:(HashmapE 32 (VarUInteger 32)) 
                 = ExtraCurrencyCollection;

currencies$_ grams:Grams other:ExtraCurrencyCollection 
           = CurrencyCollection;
```

This scheme means that in addition to the TON value, message may carry the dictionary of additional _extra-currencies_. However, currently we may neglect it and just assume that the message value is serialized as "number of nanotons as variable integer" and "`0` - empty dictionary bit".

Indeed, in the elector code above we serialize coins' amounts via `.store_coins(grams)` but then just put a string of zeros with length equal to `1 + 4 + 4 + 64 + 32 + 1 + 1`. What is it? 
* First bit stands for empty extra-currencies dictionary.
* Then we have two 4-bit long fields. They encode 0 as `VarUInteger 16`. In fact, since `ihr_fee` and `fwd_fee` will be overwritten, we may as well put there zeroes.
* Then we put zero to `created_lt` and `created_at` fields. Those fields will be overwritten as well; however, in contrast to fees, these fields have a fixed length and are thus encoded as 64- and 32-bit long strings.
* _(we had alredy serialized the message header and passed to init/body at that moment)_
* Next zero-bit means that there is no `init` field.
* The last zero-bit means that msg_body will be serialized in-place.
* After that, message body (with arbitrary layout) is encoded.

That way, instead of individual serialization of 14 parameters, we execute 4 serialization primitives.

## Full scheme
Full scheme of message layout and the layout of all constituting fields (as well as scheme of ALL objects in TON) are presented in [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb).

## Message size

:::info cell size
Note that any [Cell](/learn/overviews/cells) may contain up to `1023` bits. If you need to store more data, you should split it into chunks and store in reference cells.
:::

If, for instance, your message body size is 900 bits long, you can not store it in the same cell as the message header.
Indeed, in addition to message header fields, the total size of the cell will be more than 1023 bits, and during serialization there will be `cell overflow` exception. In this case, instead of `0` that stands for "inplace message body flag (Either)" there should be `1` and the message body should be stored in the reference cell.

Those things should be handled carefully due to the fact that some fields have variable sizes.

For instance, `MsgAddress` may be represented by four constructors: `addr_none`, `addr_std`, `addr_extern`, `addr_var` with length from 2 bits ( for `addr_none`) to 586 bits (for `addr_var` in the largest form). The same stands for nanotons' amounts which is serialized as `VarUInteger 16`. That means, 4 bits indicating the byte length of the integer and then indicated earlier bytes for integer itself. That way, 0 nanotons will be serialized as `0b0000` (4 bits which encode a zero-length byte string and then zero bytes), while 100.000.000 TON (or 100000000000000000 nanotons) will be serialized as `0b10000000000101100011010001010111100001011101100010100000000000000000` (`0b1000` stands for 8 bytes and then 8 bytes themselves).
