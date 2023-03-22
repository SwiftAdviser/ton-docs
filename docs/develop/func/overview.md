# 概述

高級語言 FunC 用於在 TON 上編程智能合約。

FunC 是一種類似於 C 語言的靜態類型的領域特定語言。

FunC 程序編譯成 Fift 組合語言代碼，該代碼生成對應的 [TON 虛擬機](https://docs.ton.dev/86757ecb2/p/299df7-tvm-overview) 的字節碼。

進一步地，這個字節碼（實際上是區塊鏈中的任何其他數據一樣的 [單元格樹](https://docs.ton.dev/86757ecb2/p/35b656-cells)）可以用於在區塊鏈上創建智能合約，也可以在本地 TVM 實例上運行。

您可以在 [文檔](https://docs.ton.dev/86757ecb2/p/42e22a-types) 部分找到有關 FunC 的更多信息。

:::info
感謝 [@akifoq](https://github.com/akifoq) 撰寫了 FunC 文檔。
:::

這裡是一個簡單的 FunC 範例方法，用於發送金錢：

```func
() send_money(slice address, int amount) impure inline {
    var msg = begin_cell()
        .store_uint(0x10, 6) ;; nobounce
        .store_slice(address)
        .store_grams(amount)
        .end_cell();

    send_raw_message(msg, 64);
}
```

## 編譯器

要在本地編譯 FunC，您需要在計算機上設置二進制文件。可以從以下位置下載 Windows、MacOS（Intel/M1）和 Ubuntu 的 FunC 編譯器二進制文件：

* [環境設置頁面](https://docs.ton.dev/86757ecb2/p/549f11-installation)

:::info 同時，您還可以總是從源代碼生成二進制文件，例如：
[FunC 編譯器源代碼](https://github.com/ton-blockchain/ton/tree/master/crypto/func)（請閱讀[如何編譯](https://docs.ton.dev/86757ecb2/p/29a8a7-how-to-compile-a-func-compiler-from-sources)從源代碼編譯 FunC 編譯器）。 :::

## 教程

:::tip 初學者提示 開始使用 FunC 的最佳地點：[介紹](https://docs.ton.dev/86757ecb2/p/27721f-introduction-to-smart-contracts) :::

其他由社區專家優雅提供的材料：

* **@romanovichim**的[在 Y 分鐘內學習 FunC](https://learnxinyminutes.com/docs/func/)
* [TON Hello World：撰寫您的第一個智能合約的逐步指南](https://ton-community.github.io/tutorials/02-contract/)
* [TON Hello World：測試您的第一個智能合約的逐步指南](https://ton-community.github.io/tutorials/04-testing/)
* **@romanovichim**的[10 FunC課程](https://github.com/romanovichim/TonFunClessons_Eng)，使用 **toncli** 和 **toncli** tests v1
* **@romanovichim**的[10 FunC課程（俄文）](https://github.com/romanovichim/TonFunClessons_ru)，使用 **toncli** 和 **toncli** tests v1
* **Vadim**的[FunC小測驗](https://t.me/toncontests/60) - 用於自我檢查。需要 10-15 分鐘。問題主要涉及 FunС，也有一些關於 TON 的一般問題。
* **Vadim**的[FunC小測驗（俄文）](https://t.me/toncontests/58?comment=14888)

## 比賽

參加[比賽](https://t.me/toncontests)是學習 FunC 的好方法。

你還可以學習過去的比賽：

* TON Smart Challenge #2 (適合初學者)： [比賽頁面](https://ton.org/ton-smart-challenge-2)、 [任務](https://github.com/ton-blockchain/func-contest2)、 [解答](https://github.com/ton-blockchain/func-contest2-solutions)、 [測試](https://github.com/ton-blockchain/func-contest2-tests)。
* TON Smart Challenge #1 (適合初學者)： [比賽頁面](https://ton.org/contest)、 [任務](https://github.com/ton-blockchain/func-contest1)、 [解答](https://github.com/ton-blockchain/func-contest1-solutions)、 [測試](https://github.com/ton-blockchain/func-contest1-tests)。

## 智能合約範例

像錢包、選民（管理 TON 上的驗證）、多簽錢包等標準基本智能合約，可以在學習時作為參考。

* [智能合約範例](https://docs.ton.dev/86757ecb2/p/6bdf29-smart-contracts-examples)

## 更改日誌

[FunC 更新歷史](https://docs.ton.dev/86757ecb2/p/28a4c2-func-changelog)。