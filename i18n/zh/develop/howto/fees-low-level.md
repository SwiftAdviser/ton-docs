# 費用（低級別）

:::caution
本節提供了與 TON 進行低級別交互的指南和手冊。
:::

本文概述了 TON 的交易費用，特別是 FunC 代碼的計算費用。在 TVM 白皮書中還有[詳細的規範](https://ton.org/tvm.pdf)。


## 交易和階段

正如[TVM 概述](/learn/tvm-instructions/tvm-overview)所述，交易執行由幾個階段組成。在這些階段中，相應的費用可能被扣除。

通常：

```cpp
transaction_fee = storage_fees
                + in_fwd_fees
                + computation_fees 
                + action_fees 
                + out_fwd_fees
```
其中：
   * `storage_fees` - 與合約在鏈狀狀態中佔用某些空間相對應的費用
   * `in_fwd_fees` - 用於將傳入消息導入區塊鏈的費用（僅適用於之前未在鏈上的消息，即`external`消息。對於來自合約到合約的普通消息，此費用不適用）
   * `computation_fees` - 對應於執行TVM指令的費用
   * `action_fees` - 與處理操作列表（發送消息，設置庫等）相關的費用
   * `out_fwd_fees` - 與將發出消息導入區塊鏈相關的費用



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


## FunC結構Gas費用

幾乎所有在FunC中使用的功能都定義在[stdlib.func](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/stdlib.fc)中，該文件將FunC功能映射到Fift組裝程序指令。 反過來，Fift組合指令被映射到[asm.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/fift/lib/Asm.fif)中的位序列指令。 因此，如果您想了解指令調用的確切成本，則需要在`stdlib.func`中查找`asm`表示，然後在`asm.fif`中查找位序列並計算指令長度（以位為單位）。


然而，通常，與位長相關的費用相對較小，而與單元格解析和創建以及跳轉和執行指令數量相關的費用相對較大。

因此，如果您想優化代碼，首先從體系結構優化開始，減少單元格解析/創建操作的次數，然後再減少跳轉的次數。

### 單元格操作
以下是一個例子，展示正確的單元格操作如何大幅減少Gas成本。

假設您想將一些編碼負載添加到發送的消息中。直觀的實現方式如下：

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

這段程式碼有什麼問題？`payload_encoding` 會先通過 `end_cell()` 創建一個單元格 (+500 gas 單位) 來生成一個切片位串，然後再解析它 `begin_parse()` (+100 gas 單位)。同樣的代碼可以通過更改一些常用類型來避免這些不必要的操作：

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
通過以另一種形式（builder而不是slice）傳遞位串，我們可以在代碼輕微更改的情況下大幅降低計算成本。

### inline 和 inline_refs
預設情況下，當您有一個FunC函數時，它會獲得自己的“id”，存儲在id->函數字典的單獨葉子中。當您在程序中的某個位置調用它時，會搜索該函數，然後進行跳轉。如果您的函數在代碼中被多次調用，則這種行為是合理的，因為跳轉可以減少代碼大小（通過僅存儲一次函數體）。

然而，如果該函數只使用一次或兩次，通常將此函數聲明為`inline`或`inline_ref`會更加節省。 `inline`修改符將函數體直接放入父函數的代碼中，而`inline_ref`則將函數代碼放入引用中（跳轉到引用仍比搜索並跳轉到字典項目要便宜得多）。

### 字典
在TON上，字典被引入為單元格（確切地說是DAG）的樹。這意味著如果您搜索、讀取或寫入字典，您需要解析相應分支的所有單元格。這意味著
   * a) 字典操作的gas成本不是固定的（因為分支中的節點大小和數量取決於給定的字典和鍵）
   * b) 通過使用特殊指令（如`replace`而不是`delete`和`add`）優化字典使用是明智的
   * c) 開發人員應該注意迭代操作（如next和prev）以及`min_key`/`max_key`操作，以避免不必要地遍歷整個字典

### 堆棧操作
請注意，FunC在幕後操作堆棧項目。這意味著代碼：
```cpp
(int a, int b, int c) = some_f();
return (c, b, a);
```
這將被翻譯為幾個指令，改變堆棧上元素的順序。

當堆棧項目的數量很大（10+），並且它們以不同的順序積極使用時，堆棧操作費用可能變得不可忽略。

## 費用計算公式

### 存儲費用

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

### 配置文件

所有費用都是以特定的 gas 數量為基礎進行命名的，並且可能會變更。配置文件代表了當前的費用成本。 


* storage_fees = [p18](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam18)
* in_fwd_fees = [p24](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam24), [p25](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam25)
* computation_fees = [p20](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam20), [p21](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam21)
* action_fees = [p24](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam24), [p25](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam25)
* out_fwd_fees = [p24](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam24), [p25](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05#configparam25)

:::info
[A direct link to the mainnet config file](https://explorer.toncoin.org/config?workchain=-1&shard=8000000000000000&seqno=22185244&roothash=165D55B3CFFC4043BFC43F81C1A3F2C41B69B33D6615D46FBFD2036256756382&filehash=69C43394D872B02C334B75F59464B2848CD4E23031C03CA7F3B1F98E8A13EE05)
:::

*Based on @thedailyton [article](https://telegra.ph/Fees-calculation-on-the-TON-Blockchain-07-24) from 24.07*