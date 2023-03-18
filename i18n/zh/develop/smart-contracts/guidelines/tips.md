# Tips & Tricks

## About bounce TON back

If you have the `throw_if` function (with code != 0) in recv_internal triggered and the bounce flag
set([tblkch.pdf 4.2.5](https://newton-blockchain.github.io/tblkch.pdf)), all coins will be sent back.

Read more in the [original discussion](https://t.me/tondev/44958).

## Payload size in bounced messages

A bounced message has only 224 bits in the body, everything else (even references) is lost.

:::info Example

1. You send `msg_body: uint112 + ^[uint112]` to a smart contract to bounce
2. SC returns bounced message with a `msg_body: 0xFFFFFFFF + uint112` **without** `^ref` payload, even though there is
   enough space for it.
:::

More info about this discussion is [here](https://t.me/tondev_eng/11201).

## About charging gas fees

This information is based on this [discussion](https://github.com/DKeysil/awesome-ton-smart-contracts/issues/1)

`accept_message` simply sets the gas limit to the maximum possible value (the gas that can be bought by both original
contract balance and message value, or, more commonly, the maximum gas amount allowed to be used in a single transaction) and
also sets the gas credit to zero.

In the case of external messages, you need to accept the message in order to make the transaction appear in the block (or,
to be more specific, you must somehow reduce your gas credit to zero). You can accept messages at any time during the TVM
execution, even after calling `send_raw_message` primitive. The only way the fees may be charged from the account is to
put a transaction into the blockchain, so it's the reason why "transactions" with no `accept_message` are "free".

In the case of internal messages, the initial gas limit is set equal to the amount of gas that can be bought by the message
value. `accept_message` raises that limit. Even without `accept_message` you can spend more coins than the message value
by sending some other messages that carry value.

Using `set_gas_limit` in internal messages does not limit the possibility of spending more TON than came with the
message when sending other messages that carry value. You can use `raw_reserve` in addition to gas limit to limit a
spendable amount of coins.

FunC docs:

- [`accept_message`](/develop/func/stdlib#accept_message)
- [`set_gas_limit`](/develop/func/stdlib#set_gas_limit)
- [`raw_reserve`](/develop/func/stdlib#raw_reserve)

Read more in the [original discussion](https://t.me/tondev/45882).

## Spend less gas on large smart contracts

`touch()` is a tip to the compiler how to best organize the stack. The command puts a variable at top of the
stack ([func docs](/develop/func/stdlib#impure_touch))

### Example

In this code:

```func
() recv_external(slice in_msg) impure {
     var signature = in_msg~load_bits(512);
     var cs = in_msg;
     var (subwallet_id, valid_until, msg_seqno) = (cs~load_uint(32), cs~load_uint(32), cs~load_uint(32));
     throw_if(36, valid_until <= now());
     var ds = get_data().begin_parse();
     var (stored_seqno, stored_subwallet, public_key, plugins) = (ds~load_uint(32), ds~load_uint(32), ds~load_uint(256), ds~load_dict());
     ds.end_parse();
     throw_unless(33, msg_seqno == stored_seqno);
     throw_unless(34, subwallet_id == stored_subwallet);
     throw_unless(35, check_signature(slice_hash(in_msg), signature, public_key));
     accept_message();
     set_data(begin_cell()
       .store_uint(stored_seqno + 1, 32)
       .store_uint(stored_subwallet, 32)
       .store_uint(public_key, 256)
       .store_dict(plugins)
       .end_cell());
     commit();
    // highlight-next-line
     cs~touch();
     int op = cs~load_uint(8);
```

`cs~touch();` will place `cs` on top of the stack, and then the interaction with the variable will be cheaper.

Read more in the [original discussion](https://t.me/tondev/45956).