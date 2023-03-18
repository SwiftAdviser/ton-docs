# Fees (low-level)

:::caution
This section describes instructions and manuals for interacting with TON at a low level.
:::

This document provides a general idea of transaction fees on TON and particularly computation fees for the FunC code. There is also a [detailed specification in the TVM whitepaper](https://ton.org/tvm.pdf).

## Transactions and phases

As was described in the [TVM overview](/learn/tvm-instructions/tvm-overview), transaction execution consists of a few phases. During those phases, the corresponding fees may be deducted.

Generally:
```cpp
transaction_fee = storage_fees
                + in_fwd_fees
                + computation_fees 
                + action_fees 
                + out_fwd_fees
```
where:
   * `storage_fees`—fees corresponding to occupation of some space in chain state by contract
   * `in_fwd_fees`—fees for importing to blockchain incoming message (it is only relevant for messages which were not previously on-chain, that is, `external` messages. For ordinary messages from contract to contract this fee is not applicable)
   * `computation_fees`—fees corresponding to execution of TVM instructions
   * `action_fees`—fees related to processing of action list (sending messages, setting libraries etc.)
   * `out_fwd_fees`—fees related to importing to blockchain of outcoming message

## Computation fees

### Gas
All computation costs are nominated in gas units. The price of gas units is determined by this chain config (Config 20 for masterchain and Config 21 for basechain) and may be changed only by consensus of the validator. Note that unlike in other systems, the user cannot set his own gas price, and there is no fee market.

Current settings in basechain are as follows: 1 unit of gas costs 1000 nanotons.

## TVM instructions cost
On the lowest level (TVM instruction execution) the gas price for most primitives
equals the _basic gas price_, computed as `P_b := 10 + b + 5r`,
where `b` is the instruction length in bits and `r` is the
number of cell references included in the instruction.

Apart from those basic fees, the following fees appear:

| Instruction             | GAS  price   | Description                                                                                                                                                                                   | 
|-------------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Creation of cell        | **500**      | Operation of transforming builder to cell.                                                                                                                                                    |
| Parsing cell firstly    | **100**      | Operation of transforming cells into slices first time during current transaction.                                                                                                            | 
| Parsing cell repeatedly | **25**       | Operation of transforming cells into slices, which already has parsed during same transaction.                                                                                                |
| Throwing exception      | **50**       |                                                                                                                                                                                               | 
| Operation with tuple    | **1**        | This price will multiply by the quantity of tuple's elements.                                                                                                                                 | 
| Implicit Jump           | **10**       | It is paid when all instructions in the current continuation cell are executed. However, there are references in that continuation cell, and the execution flow jumps to the first reference. | 
| Implicit Back Jump      | **5**        | It is paid when all instructions in the current continuation are executed and execution flow jumps back to the continuation from which the just finished continuation was called.             |                                                                                      
| Moving stack elements   | **1**        | Price for moving stack elements between continuations. It will charge correspond gas price for every element. However, the first 32 elements moving is free.                                  |                                                                                       


## FunC constructions gas fees

Almost all functions used in FunC are defined in [stdlib.func](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/stdlib.fc) which maps FunC functions to Fift assembler instructions. In turn, Fift assembler instructions are mapped to bit-sequence instructions in [asm.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/fift/lib/Asm.fif). So if you want to understand how much exactly the instruction call will cost you, you need to find `asm` representation in `stdlib.func`, then find bit-sequence in `asm.fif` and calculate instruction length in bits.

However, generally, fees related to bit-lengths are minor in comparison with fees related to cell parsing and creation, as well as jumps and just number of executed instructions.

So, if you try to optimize your code start with architecture optimization, the decreasing number of cell parsing/creation operations, and then with the decreasing number of jumps.

### Operations with cells
Just an example of how proper cell work may substantially decrease gas costs.

Let''s imagine that you want to add some encoded payload to the outgoing message. Straightforward implementation will be as follows:
```cpp
slice payload_encoding(int a, int b, int c) {
  return
    begin_cell().store_uint(a,8)
                .store_uint(b,8)
                .store_uint(c,8)
    end_cell().begin_parse();
}

() send_message(slice destination) impure {
  slice payload = payload_encoding(1, 7, 12);
  var msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(destination)
    .store_coins(0)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; some flags related to message header
    .store_uint(0x33bbff77, 32) ;; op-code (see smart-contract guidelines)
    .store_uint(cur_lt(), 64)  ;; query_id (see smart-contract guidelines)
    .store_slice(payload)
  .end_cell();
  send_raw_message(msg, 64);
}
```

What is the problem with this code? `payload_encoding` to generate a slice bit-string, first create a cell via `end_cell()` (+500 gas units). Then parse it `begin_parse()` (+100 gas units). The same code can be written without those unnecessary operations by changing some commonly used types:

```cpp
;; we add asm for function which stores one builder to the another, which is absent from stdlib
builder store_builder(builder to, builder what) asm(what to) "STB";

builder payload_encoding(int a, int b, int c) {
  return
    begin_cell().store_uint(a,8)
                .store_uint(b,8)
                .store_uint(c,8);
}

() send_message(slice destination) impure {
  builder payload = payload_encoding(1, 7, 12);
  var msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(destination)
    .store_coins(0)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; some flags related to message header
    .store_uint(0x33bbff77, 32) ;; op-code (see smart-contract guidelines)
    .store_uint(cur_lt(), 64)  ;; query_id (see smart-contract guidelines)
    .store_builder(payload)
  .end_cell();
  send_raw_message(msg, 64);
}
```
By passing bit-string in the another form (builder instead of slice) we substantially decrease computation cost by very slight change in code.

### Inline and inline_refs
By default, when you have a FunC function, it gets its own `id`, stored in a separate leaf of id->function dictionary, and when you call it somewhere in the program, a search of the function in dictionary and subsequent jump occur. Such behavior is justified if your function is called from many places in the code and thus jumps allow to decrease the code size (by storing a function body once). However, if the function is only used once or twice, it is often much cheaper to declare this function as `inline` or `inline_ref`. `inline` modificator places the body of the function right into the code of the parent function, while `inline_ref` places the function code into the reference (jumping to the reference is still much cheaper than searching and jumping to the dictionary entry).

### Dictionaries
Dictionaries on TON are introduced as trees (DAGs to be precise) of cells. That means that if you search, read, or write to the dictionary, you need to parse all cells of the corresponding branch of the tree. That means that
   * a) dicts operations are not fixed in gas costs (since the size and number of nodes in the branch depend on the given dictionary and key)
   * b) it is expedient to optimize dict usage by using special instructions like `replace` instead of `delete` and `add`
   * c) developer should be aware of iteration operations (like next and prev) as well `min_key`/`max_key` operations to avoid unnecessary iteration through the whole dict

### Stack operations
Note that FunC manipulates stack entries under the hood. That means that the code:
```cpp
(int a, int b, int c) = some_f();
return (c, b, a);
```
will be translated into a few instructions which changes the order of elements on the stack.

When the number of stack entries is substantial (10+), and they are actively used in different orders, stack operations fees may become non-negligible.

## Fee's calculation Formulas

### storage_fees
```cpp
storage_fees = ceil(
                    (account.bits * bit_price
                    + account.cells * cell_price)
               * period / 2 ^ 16)
```
### in_fwd_fees, out_fwd_fees

```cpp
msg_fwd_fees = (lump_price
             + ceil(
                (bit_price * msg.bits + cell_price * msg.cells) / 2^16)
             )
             
ihr_fwd_fees = ceil((msg_fwd_fees * ihr_price_factor) / 2^16)
```
// bits in the root cell of a message are not included in msg.bits (lump_price pays for them)

### action_fees
```cpp
action_fees = sum(out_ext_msg_fwd_fee) + sum(int_msg_mine_fee)
```

### Config file

All fees are nominated for a certain gas amount and may be changed. The config file represents the current fee cost.

* storage_fees = [p18](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam18)
* in_fwd_fees = [p24](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam24), [p25](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam25)
* computation_fees = [p20](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam20), [p21](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam21)
* action_fees = [p24](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam24), [p25](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam25)
* out_fwd_fees = [p24](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam24), [p25](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam25)

:::info
[A direct link to the mainnet config file](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05)
:::

*Based on @thedailyton [article](https://telegra.ph/Fees-calculation-on-the-TON-Blockchain-07-24) from 24.07*