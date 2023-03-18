# Messages TL-B schemes

In this section detailed explanation of TL-B schemes for messages.


## Message TL-B
### TL-B
Main message TL-B scheme declared as a combination of several nested structures

```tlb
message$_ {X:Type} info:CommonMsgInfo
init:(Maybe (Either StateInit ^StateInit))
body:(Either X ^X) = Message X;

message$_ {X:Type} info:CommonMsgInfoRelaxed
init:(Maybe (Either StateInit ^StateInit))
body:(Either X ^X) = MessageRelaxed X;

_ (Message Any) = MessageAny;
```

Here `Message X` - is common message structure, `MessageRelaxed X` additional type with CommonMsgInfoRelaxed body and `Message Any` is a union of both.
Message structure unified with X:Type, that in other words is a Cell.
According to TL-B we can combine all data in one cell(if it will be fit to 1023 bits) or use references declared with caret `^`.

Serialized `Message X` placed to action list with FunC method send_raw_message(), than smart contract execute this action and message send.


### Definition of explicit serialization
For building valid binary data according TL-B structure we should do serialization, which defined for each type recurrently. It means, that for serialization of Message X we need to know how to serialize
`StateInit`, `CommonMsgInfo` and so on.

Every nested structure we should get from another TL-B scheme according to link recurrently, until serialization for top structure will be explicit - every bit defined by Boolean or bit-like type(bits, uint, varuint).

Structures that currently does not use in regular development will mark with `*` in Type column, for example *Anycast usually skipped in serialization.


### message$_

There is the top TL-B scheme whole messages `Message X`:

```tlb
message$_ {X:Type} info:CommonMsgInfo
init:(Maybe (Either StateInit ^StateInit))
body:(Either X ^X) = Message X;
```


| Structure | Type                              | Required | Description                                                                                                    |
|-----------|-----------------------------------|----------|----------------------------------------------------------------------------------------------------------------|
| message$_ | Constructor                       |          | It defined according the constructor ruler. Empty tag `$_` means we will not add any bits in the beginning     |
| info      | [CommonMsgInfo](#commonmsginfo)   | Required | Detailed Message properties define destination and its value. Always placed in message root cell.              |
| init      | [StateInit](#stateinit-tl-b)      | Optional | General structure using in TON for initilizing new contracts. Could be write in cell reference or root cell.   |
| body      | X                                 | Required | Message Payload. Could be write in cell reference or root cell.                                                |                                                                                            |


```tlb
nothing$0 {X:Type} = Maybe X;
just$1 {X:Type} value:X = Maybe X;
left$0 {X:Type} {Y:Type} value:X = Either X Y;
right$1 {X:Type} {Y:Type} value:Y = Either X Y;
```

Recall how `Maybe` and `Either` works, we can serialize different cases:

* `[CommonMsgInfo][10][StateInit][0][X]` - `Message X` in the one cell

![TL-B example](/img/docs/data-formats/tl-b-docs-9.png?raw=true)

* `[CommonMsgInfo][11][^StateInit][1][^X]` - `Message X` with references

![TL-B example](/img/docs/data-formats/tl-b-docs-8.png?raw=true)



## CommonMsgInfo TL-B

### CommonMsgInfo

`CommonMsgInfo` is a list of parameters, that defines how message will be delivered in TON blockchain.


```tlb
//internal message
int_msg_info$0 ihr_disabled:Bool bounce:Bool bounced:Bool
  src:MsgAddressInt dest:MsgAddressInt 
  value:CurrencyCollection ihr_fee:Grams fwd_fee:Grams
  created_lt:uint64 created_at:uint32 = CommonMsgInfo;
  
//external incoming message  
ext_in_msg_info$10 src:MsgAddressExt dest:MsgAddressInt 
  import_fee:Grams = CommonMsgInfo;
  
//external outgoing message
ext_out_msg_info$11 src:MsgAddressInt dest:MsgAddressExt
  created_lt:uint64 created_at:uint32 = CommonMsgInfo;
```

### int_msg_info$0

`int_msg_info` is a case of internal message. This means they could be sent between contracts, and only between contracts.
Use case - ordinary cross contract messages.


```tlb
nanograms$_ amount:(VarUInteger 16) = Grams;
//internal message
int_msg_info$0 ihr_disabled:Bool bounce:Bool bounced:Bool
  src:MsgAddressInt dest:MsgAddressInt 
  value:CurrencyCollection ihr_fee:Grams fwd_fee:Grams
  created_lt:uint64 created_at:uint32 = CommonMsgInfo;
```

| Structure      | Type                                       | Required | Description                                                                                                         |
|----------------|--------------------------------------------|----------|---------------------------------------------------------------------------------------------------------------------|
| int_msg_info$0 | Constructor                                | Required | $0 tag means, that in serialization CommonMsgInfo started with 0 bit describes a internal message.                  |
| ihr_disabled   | Bool                                       | Required | Hyper cube routing flag.                                                                                            |
| bounce         | Bool                                       | Required | Message should be bounced if there are errors during processing. If message's flat bounce = 1, it calls bounceable. |
| bounced        | Bool                                       | Required | Flag that describes, that message itself is a result of bounce.                                                     |       
| src            | [MsgAddressInt](#msgaddressint-tl-b)       | Required | Address of smart contract sender of message.                                                                        |
| dest           | [MsgAddressInt](#msgaddressint-tl-b)       | Required | Address of smart contract destination of message.                                                                   |
| value          | [CurrencyCollection](#currencycollection)  | Required | Structure which describes currency information including total funds transferred in message.                        |
| ihr_fee        | [VarUInteger 16](#varuinteger-n)           | Required | Fees for hyper routing delivery                                                                                     |
| fwd_fee        | [VarUInteger 16](#varuinteger-n)           | Required | Fees for forwarding messages assigned by validators                                                                 |
| created_lt     | uint64                                     | Required | Logic time of sending message assigned by validator. Using for odering actions in smart contract.                   |
| created_at     | uint32                                     | Required | Unix time                                                                                                           |



### ext_in_msg_info$10

`ext_in_msg_info$10` is a case of external incoming message. This means this type of messages sent from contracts to off-chain space.\
Use case - wallet application request to wallet contract.


```tlb
nanograms$_ amount:(VarUInteger 16) = Grams;
//external incoming message  
ext_in_msg_info$10 src:MsgAddressExt dest:MsgAddressInt 
  import_fee:Grams = CommonMsgInfo;
```

| Structure           | Type                                 | Required | Description                                                                                                        |
|---------------------|--------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------|
| ext_out_msg_info$10 | Constructor                          | Required | `$10` tag means, that in serialization CommonMsgInfo started with `10` bits describes a external incoming message. |
| ihr_disabled        | Bool                                 | Required | Hyper routing flag. (currently always true)                                                                        |
| src                 | [MsgAddressExt](#msgaddressext-tl-b) | Required | Address of a external sender of the message.                                                                       |
| dest                | [MsgAddressInt](#msgaddressint-tl-b) | Required | Address of smart contract destination of message.                                                                  |
| import_fee          | [VarUInteger 16](#varuinteger-n)     | Required | Fee for executing and delivering of message.                                                                       |


### ext_in_msg_info$11

`ext_out_msg_info$11` is a case of external outgoing message. This means they could be sent from contracts to off-chain space.
Use case - logs.

```tlb
//internal message
ext_out_msg_info$11 src:MsgAddressInt dest:MsgAddressExt
  created_lt:uint64 created_at:uint32 = CommonMsgInfo;
```

| Structure           | Type                                  | Required | Description                                                                                                       |
|---------------------|---------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| ext_out_msg_info$11 | Constructor                           | Required | `$11` tag means, that in serialization CommonMsgInfo started with `11` bit describes a external outgoing message. |
| src                 | [MsgAddressInt](#msgaddressint-tl-b)  | Required | Hyper routing flag. v                                                                                             |
| dest                | [MsgAddressExt](#msgaddressext-tl-b)  | Required | General structure using in TON for initializing new contracts. Could be write in cell reference or root cell.     |
| created_lt          | uint64                                | Required | Logic time of sending message assigned by validator. Using for odering actions in smart contract.                 |
| created_at          | uint32                                | Required | Unix time                                                                                                         |


## StateInit TL-B

StateInit serves to delivery inital data to contract and used in contract deployment.

```tlb
_ split_depth:(Maybe (## 5)) special:(Maybe TickTock)
  code:(Maybe ^Cell) data:(Maybe ^Cell)
  library:(HashmapE 256 SimpleLib) = StateInit;
```



| Structure   | Type                    | Required | Description                                                                                                                                            |
|-------------|-------------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| split_depth | (## 5)                  | Optional | Parameter for the highload contracts, defines behaviour of splitting into multiple instances in different shards. Currently StateInit used without it. |
| special     | TickTock*               | Optional | Used for invoking smart contracts in every new block of the blockchain. Available only in the masterchain. Regular user's contracts used without it.   |
| code        | Cell                    | Optional | Contract's serialized code.                                                                                                                            |
| data        | Cell                    | Optional | Contract initial data.                                                                                                                                 |       
| library     | HashmapE 256 SimpleLib* | Optional | Currently used StateInit without libs                                                                                                                  |


[General detailed explanations for Hashmaps](../data-formats/tl-b#hashmap)



## MsgAddressExt TL-B


```tlb
addr_none$00 = MsgAddressExt;
addr_extern$01 len:(## 9) external_address:(bits len)
= MsgAddressExt;
```

`MsgAddress` is a scheme of various serialization for addresses. Depends on which participant(off-chain or smartcontract) messages sent, different structures using.

### addr_none$00

`addr_none$00` - using for defining null address of off-chain participant. It means, that we can send external message to contract without unique sender's address.

```tlb
addr_none$00 = MsgAddressExt;
```

| Structure           | Type               | Required | Description                                                                                                             |
|---------------------|--------------------|----------|-------------------------------------------------------------------------------------------------------------------------|
| ext_out_msg_info$11 | Constructor        | Required | `$00` tag means, that in serialization MsgAddressExt started with `00` bits. This means whole external address is `00`. |


### addr_extern$01

```tlb
addr_extern$01 len:(## 9) external_address:(bits len)
= MsgAddressExt;
```


| Structure        | Type        | Required | Description                                                                                                      |
|------------------|-------------|----------|------------------------------------------------------------------------------------------------------------------|
| addr_extern$01   | Constructor | Required | `$01` tag means, that in the serialization MsgAddressExt started with a `01` bits describes an external address. |
| len              | ## 9        | Required | Same as uintN - means an unsigned N-bit number                                                                   |
| external_address | (bits len)  | Required | Address is a bitstring of the len equal to previous `len`                                                        |


## MsgAddressInt TL-B

```tlb
addr_std$10 anycast:(Maybe Anycast)
workchain_id:int8 address:bits256  = MsgAddressInt;

addr_var$11 anycast:(Maybe Anycast) addr_len:(## 9)
workchain_id:int32 address:(bits addr_len) = MsgAddressInt;
```

### addr_std$10

```tlb
addr_std$10 anycast:(Maybe Anycast)
workchain_id:int8 address:bits256  = MsgAddressInt;
```


| Structure    | Type        | Required | Description                                                                                                      |
|--------------|-------------|----------|------------------------------------------------------------------------------------------------------------------|
| addr_std$10  | Constructor | Required | `$10` tag means, that in the serialization MsgAddressExt started with a `10` bits describes an external address. |
| anycast      | Anycast*    | Optional | Additional address data, currently do not used in ordinary internal messages                                     |
| workchain_id | int8        | Required | Workchain where smart contract of destination address placed. At moment always equals zero.                      |
| address      | (bits256)   | Required | Smart contract account ID number                                                                                 |



### addr_var$11

```tlb
addr_var$11 anycast:(Maybe Anycast) addr_len:(## 9)
workchain_id:int32 address:(bits addr_len) = MsgAddressInt;
```




| Structure    | Type        | Required  | Description                                                                                                               |
|--------------|-------------|-----------|---------------------------------------------------------------------------------------------------------------------------|
| addr_var$11  | Constructor | Required  | `$11` tag means, that in the serialization MsgAddressInt started with a `11` bits describes an internal contract address. |
| anycast      | Anycast*    | Optional  | Additional address data, currently do not used in ordinary internal messages                                              |
| addr_len     | ## 9        | Required  | Same as uintN - means an unsigned N-bit number                                                                            |
| workchain_id | int32       | Required  | Workchain where smart contract of destination address placed. At moment always equals zero.                               |
| address      | (bits256)   | Required  | Payload address(could be account ID)                                                                                      |


## Basic used types


### CurrencyCollection

```tlb
nanograms$_ amount:(VarUInteger 16) = Grams;
currencies$_ grams:Grams other:ExtraCurrencyCollection
= CurrencyCollection;
```



| Structure    | Type                    | Required | Description                                                                                                  |
|--------------|-------------------------|----------|--------------------------------------------------------------------------------------------------------------|
| currencies$_ | Constructor             | Required | `$_` empty tag means, that in the serialization CurrencyCollection we will not add any bits in the beginning |
| grams        | (VarUInteger 16)        | Required | Message value in nanoTons                                                                                    |
| other        | ExtraCurrencyCollection | Optional | ExtraCurrencyCollection is a dict designed for additional currencies, that usually empty                     |

* ExtraCurrencyCollection complex type, that usually wrote as empty dict in messages


### VarUInteger n

```tlb
var_uint$_ {n:#} len:(#< n) value:(uint (len * 8))
= VarUInteger n;
var_int$_ {n:#} len:(#< n) value:(int (len * 8))
= VarInteger n;
```



| Structure  | Type             | Required | Description                                                                                                          |
|------------|------------------|----------|----------------------------------------------------------------------------------------------------------------------|
| var_uint$_ | Constructor      | Required | `var_uint$_` empty tag means, that in the serialization CurrencyCollection we will not add any bits in the beginning |
| len        | uintN            | Required | bits len parameter for next value                                                                                    |
| value      | (uint (len * 8)) | Optional | uint value for integer number wrote in (len * 8) bits                                                                |


## Message example

### Regular func internal message

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
### Regular func message in short form

Message parts that are always overwritten by validators could be skipped(fill with zero bits). Message's sender here skipped too, serialized as `addr_none$00`.

```func
  cell msg = begin_cell()
        .store_uint(0x18, 6)
        .store_slice(addr)
        .store_coins(amount)
        .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
        .store_slice(message_body)
.end_cell();
```