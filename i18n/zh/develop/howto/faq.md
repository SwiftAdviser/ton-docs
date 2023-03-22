## 概述

### 能否簡要介紹一下 TON？

- [介紹開放網絡](/learn/introduction)
- [TON Blockchain基於PoS共識](https://blog.ton.org/the-ton-blockchain-is-based-on-pos-consensus)
- [TON白皮書](/learn/docs)


## 常見問題解答

本節介紹 TON Blockchain 最常見的問題和解答。

## 概述

### 能否簡要介紹一下 TON？

- [介紹開放網絡](/learn/introduction)
- [TON Blockchain基於PoS共識](https://blog.ton.org/the-ton-blockchain-is-based-on-pos-consensus)
- [TON白皮書](/learn/docs)

### 與 EVM 鏈相比的相似之處和不同之處？

- [以太坊到 TON](/learn/introduction#ethereum-to-ton)

### TON 是否有測試環境？

- [測試網](/develop/smart-contracts/environment/testnet)

## 區塊

### 用於檢索區塊信息的 RPC 方法是什麼？ 


驗證器產生的塊。現有塊通過Liteserver可用。 Liteserver通過Liteclient訪問。 基於Liteclient建立的第三方工具，如錢包，探索器，dapp等。

- Liteclient核心：[ton-blockchain/tonlib](https://github.com/ton-blockchain/ton/tree/master/tonlib)


第三方高級區塊探測器：
- [開發者的探測器](/participate/explorers)
- https://toncenter.com/
- https://ton.app/explorers


### 區塊時間

_2-5s_

:::info
Read more at [ton.org/analysis](https://ton.org/analysis).
:::

### 時間至確定性（Time-to-finality）

_Under 6 sec._

:::info
Read more at [ton.org/analysis](https://ton.org/analysis).
:::

### 平均區塊大小

```bash 
max block size param 29
max_block_bytes:2097152
```

:::info
在[網絡配置](/develop/howto/network-configs)中查找更多實際的參數。
:::

### 區塊架構是什麼？

- [區塊布局](https://ton.org/docs/tblkch.pdf#page=96&zoom=100,148,172)，TON區塊鏈，第96頁

## 交易

### 獲取交易數據的RPC方法


- [see answer above](/develop/getting-started#what-is-the-rpc-method-used-to-retrieve-block-information)

### Is it async or synchronous? If async, any documentation on how it works?

TON Blockchain是非同步的:
- 發送者準備交易並通過liteclient（或更高級別的工具）廣播它
- Liteclient返回廣播的狀態，而不是交易結果
- 發送者檢查所需結果

錢包合約轉帳的示例（高級別）：
- [如何使用JavaScript訪問TON錢包的工作原理以及如何訪問它們](https://blog.ton.org/how-ton-wallets-work-and-how-to-access-them-from-javascript#1b-sending-a-transfer)

錢包合約轉帳的示例（低級別）：
- https://github.com/xssnick/tonutils-go/blob/master/example/wallet/main.go

### 我們如何確定交易是否真正成功？只查詢交易級別的狀態是否足夠？

**簡短回答：** 檢查接收方的帳戶狀態是否發生變化，直到它變化，請參見以下示例：
- Go: [錢包示例](https://github.com/xssnick/tonutils-go/blob/master/example/wallet/main.go)
- Python: [帶有TON支付的商店機器人](/develop/dapps/tutorials/accept-payments-in-a-telegram-bot)
- JavaScript: [售賣餃子的機器人](/develop/dapps/tutorials/accept-payments-in-a-telegram-bot-js)

### 交易的架構是什麼？

基礎知識：

- https://ton.org/docs/tblkch.pdf#page=75&zoom=100,148,290 p.75

來自explorers的例子（轉移交易）：
- https://tonscan.org/tx/FiR7bn5LuBO0FYjx7Fst9kuwnXs128NVFA9YYniKG-A=
- https://ton.cx/tx/33513508000001:FiR7bn5LuBO0FYjx7Fst9kuwnXs128NVFA9YYniKG+A=:EQBfAN7LfaUYgXZNw5Wc7GBgkEX2yhuJ5ka95J1JJwXXf4a8


### 是否可以批次處理交易？

是的，有兩種方式可以實現批次處理交易：
- 利用TON的異步性質，即將獨立的交易發送到網絡中
- 使用智能合約接收任務，然後作為一批執行它們

使用批量處理合約的示例（高負載錢包）：
- https://github.com/tonuniverse/highload-wallet-api

## 標準

### TON支援哪些貨幣的精度？

_9位數_

:::info
主網支援的小數位數：9位數。
:::

### 有沒有代幣和NFT的標準？即從交易解析可轉讓和不可轉讓代幣的標準方式

NFTs：
- [TEP-62：NFT標準](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)
- [有關NFT的文檔](/develop/dapps/defi/tokens#nft)

Jettons（代幣）：
- [TEP-74：Jettons標準](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)
- [分佈式TON代幣概述](https://telegra.ph/Scalable-DeFi-in-TON-03-30)
- [有關Jettons的文檔](/develop/dapps/defi/tokens#jettons)

其他標準：
- https://github.com/ton-blockchain/TEPs

### 是否有解析這些事件的示例

TON中的所有內容都是boc消息，因此使用NFT不是一個特殊事件，它是來自/到合約的常規消息，就像一個普通的錢包一樣。

但是，某些索引API允許您查看所有從/到合約的消息，因此您可以根據需要對它們進行篩選：

- https://tonapi.io/swagger-ui


### 也請分享如何獲取這些事件的模式。

https://ton.org/docs/tblkch.pdf#page=53&zoom=100,148,172
p.53

## 帳戶結構

### 地址格式是什麼？

- [智能合約地址](/learn/overviews/addresses)

### 是否可以有類似於ENS的命名帳戶？

可以，使用TON DNS：
- [什麼是TON DNS？](/learn/services/dns)

### 如何區分普通帳戶和智能合約？

- [一切都是智能合約](/learn/overviews/addresses#everything-is-a-smart-contract)

### 如何判斷地址是否是代幣地址？

對於 **Jettons** 合約必須實現 [標準介面](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) 並在 _get_wallet_data()_ 或 _get_jetton_data()_ 方法中返回數據。

### 是否有任何特殊的帳戶（例如由網路擁有）有與其他帳戶不同的規則或方法？

在 TON 中有一個稱為 masterchain 的特殊區塊鏈。它由全網範圍的合約組成，包括網路配置、驗證器相關合約等：

:::info
了解更多關於 TON 區塊鏈概述的文章：[區塊鏈的區塊鏈](/learn/overviews/ton-blockchain)。
:::

一個很好的例子是智能治理合約，它是 masterchain 的一部分：
- [治理合約](/develop/smart-contracts/governance)

## 智能合約

### 如何偵測合約部署事件？

[TON 中的一切都是智能合約](/learn/overviews/addresses#everything-is-a-smart-contract)。

帳戶地址是由 _私鑰_、_合約代碼_ 和 _初始狀態_ 生成的。

如果有任何一個組件更改，地址會相應地更改。智能合約代碼本身可以稍後發送到網絡上。

為了防止向不存在的合約發送消息，TON 使用了 "bounce" 功能。請閱讀以下文章以獲取更多資訊：

- [通過 TonLib 部署錢包](https://ton.org/docs/develop/dapps/asset-processing/#deploying-wallet)
- [支付處理請求和發送響應的費用](https://ton.org/docs/develop/smart-contracts/guidelines/processing)
- [技巧提示：反彈 TON](https://ton.org/docs/develop/smart-contracts/guidelines/tips)

### 是否可以將代碼重新部署到現有地址，還是必須將其作為新合約部署？

是的，這是可能的。如果智能合約實現了方法......它的代碼可以更新，地址將保持不變。

- https://ton.org/docs/tblkch.pdf#page=30&zoom=100,148,685 p.30

:::info 順帶一提
可以使用相同的私鑰* 部署具有不同地址的多個合約。
:::

### 智能合約地址區分大小寫嗎？

是的，智能合約地址區分大小寫，因為它們是使用 [base64 算法](https://en.wikipedia.org/wiki/Base64) 生成的。 您可以在 [這裡](/docs/learn/overviews/addresses) 了解有關智能合約地址的更多信息。

## RPC

### 提供一個建議的節點提供者列表以進行數據提取

API類型:
- 了解有關不同 [API類型](/develop/dapps/apis/) 的更多信息（索引，HTTP和ADNL）

節點提供者合作夥伴：

- [getblock.io](https://getblock.io/)

包含 TON 社區項目的 TON 目錄：

- [ton.app](https://ton.app/)

### 是否有任何公共節點端點，我們可以開始探索鏈（主網和測試網）

- [網絡配置](/develop/howto/network-configs)
- [示例和教程](/develop/dapps/#examples)