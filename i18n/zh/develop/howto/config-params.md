# 配置參數

:::caution
本節介紹與TON進行低級交互的說明和手冊。
:::

本文檔的目的是為TON區塊鏈的配置參數提供基本解釋，並給出由大多數驗證器共識進行更改這些參數的分步指南。我們假設讀者已經熟悉Fift和Lite Client，如在 [LiteClient-HOWTO](https://toncoin.org/#/howto/step-by-step) 中所解釋的，以及在描述驗證器對配置建議投票的部分中的 [FullNode-HOWTO](https://toncoin.org/#/howto/full-node) 和 [Validator-HOWTO](https://toncoin.org/#/howto/validator)。


## 1. 配置參數
**配置參數**是影響TON區塊鏈驗證器和/或基本智能合約行為的某些值。所有配置參數的當前值存儲在主鏈狀態的特殊部分，並在需要時從當前主鏈狀態中提取。因此，有意義的是討論相對於某個主鏈區塊的配置參數的值。每個分片鏈區塊都包含對最新已知主鏈區塊的引用；假設對應的主鏈狀態中的值對此分片鏈區塊有效並在其生成和驗證期間使用。對於主鏈區塊，使用先前主鏈區塊的狀態來提取活動配置參數。因此，即使有人試圖在主鏈區塊內更改某些配置參數，更改也只會對下一個主鏈區塊生效。

每個配置參數由一個帶符號的32位整數索引標識，稱為**配置參數索引**或簡單地稱為**索引**。配置參數的值始終是一個單元(Cell)。某些配置參數可能會丟失；然後有時假設該參數的值為`Null`。還有一個**必需**配置參數列表，必須始終存在；此列表存儲在配置參數`#10`中。

所有配置參數都組合成一個**配置字典** - 一個具有帶符號的32位鍵（配置參數索引）和僅由一個單元引用組成的值的Hashmap。換句話說，配置字典是TL-B類型的值（`HashmapE 32 ^Cell`）。實際上，所有配置參數的集合以TL-B類型`ConfigParams`的值存儲在主鏈狀態中：

    _ config_addr:bits256 config:^(Hashmap 32 ^Cell) = ConfigParams;

我們看到，除了配置字典外，`ConfigParams`包含`config_addr` ——主鏈中配置智能合約的256位地址。稍後將提供有關配置智能合約的更多詳細信息。

包含所有配置參數的活動值的配置字典在執行事務中執行其代碼的所有智能合約中都可以通過特殊的TVM寄存器`c7`獲得。更確切地說，當執行智能合約時，`c7`由一個元組初始化，其唯一元素是包含幾個對執行智能合約有用的“上下文”值的元組，例如當前的Unix時間（如在區塊標頭中註冊）。這個元組的第十個條目（即，具有從零開始的索引9的條目）包含表示配置字典的單元。因此，可以通過TVM指令`PUSH c7; FIRST; INDEX 9`或等效指令`CONFIGROOT`訪問它。實際上，特殊的TVM指令`CONFIGPARAM`和`CONFIGOPTPARAM`將先前的操作與字典查找結合在一起，通過其索引返回任何配置參數。我們參考TVM文檔以獲取有關這些指令的更多詳細信息。這裡的關鍵是所有配置參數都可以輕鬆地從所有智能合約（主鏈或分片鏈）訪問，並且智能合約可以檢查它們並使用它們進行特定檢查。例如，智能合約可以從配置參數中提取工作鏈數據存儲價格，以計算存儲用戶提供的數據塊的價格。


配置參數的值並非任意的。實際上，如果配置參數索引`i`是非負的，那麼該參數的值必須是TL-B類型的有效值（`ConfigParam i`）。驗證器會強制執行此限制，除非它們是相應TL-B類型的有效值，否則它們不會接受對非負索引的配置參數的更改。

因此，這些參數的結構在源文件`crypto/block/block.tlb`中確定，其中為`i`的不同值定義了（`ConfigParam i`）。例如，

    _ config_addr:bits256 = ConfigParam 0;
    _ elector_addr:bits256 = ConfigParam 1;
    _ dns_root_addr:bits256 = ConfigParam 4;  // root TON DNS resolver

    capabilities#c4 version:uint32 capabilities:uint64 = GlobalVersion;
    _ GlobalVersion = ConfigParam 8;  // all zero if absent

我們看到配置參數`#8`包含一個沒有引用並確切有104個數據位的單元(Cell)。前四位必須是`11000100`，然後存儲了32位，其中包含當前啟用的“全局版本”，後面是與當前啟用的功能對應的64位整數標記。關於所有配置參數的更詳細描述將在TON區塊鏈文檔的附錄中提供；目前，可以檢查`crypto/block/block.tlb`中的TL-B方案，並檢查驗證器源代碼中如何使用不同的參數。

與非負索引的配置參數相反，負索引的配置參數可以包含任意值。至少，驗證器不強制執行對它們的值的限制。因此，它們可以用於存儲重要信息（例如某些智能合約必須開始運行的Unix時間），這些信息對於區塊生成並非關鍵，但是由一些基本智能合約使用。


## 2. 更改配置參數

我們已經解釋過，配置參數的當前值存儲在主鏈狀態的一個特殊部分。它們是如何被更改的呢？

實際上，主鏈上有一個特殊的智能合約，稱為**配置智能合約**。它的地址由我們之前描述過的`ConfigParams`中的`config_addr`字段確定。其數據中的第一個單元(Cell)引用必須包含所有配置參數的最新副本。當生成新的主鏈區塊時，將通過其地址`config_addr`查找配置智能合約，並從其數據的第一個單元引用中提取新的配置字典。經過一些有效性檢查（例如驗證具有非負32位索引`i`的任何值確實是TL-B類型（`ConfigParam i`）的有效值）後，驗證器將此新配置字典復制到包含ConfigParams的主鏈部分。此操作在創建所有交易之後執行，因此只檢查配置智能合約中存儲的新配置字典的最終版本。如果有效性檢查失敗，則“真實”的配置字典保持不變。通過這種方式，配置智能合約無法安裝配置參數的無效值。如果新配置字典與當前配置字典相符，則不執行任何檢查，也不進行任何更改。

這樣，所有對配置參數的更改都是由配置智能合約執行的，並且是其代碼確定了更改配置參數的規則。目前，配置智能合約支持兩種更改配置參數的模式：

1) 通過使用與存儲在配置智能合約數據中的公鑰對應的特定私鑰簽名的外部消息。這是公共測試網絡以及可能由一個實體控制的較小私有測試網絡中使用的方法，因為它使操作者可以輕鬆更改任何配置參數的值。請注意，這個公鑰可以通過一個由舊鑰匙簽名的特殊外部消息來更改，如果它被更改為零，那麼這個機制將被禁用。因此，可以在啟動後立即使用它進行微調，然後永久禁用它。
2) 通過創建“配置提案”，然後由驗證者投票贊成或反對。通常，配置提案必須收集來自超過3/4的所有驗證者（按權重）的投票，並且不僅在一個回合中，而且在幾個回合中（即，幾個連續的驗證者集合必須確認所提出的參數更改）。這是TON區塊鏈主網將使用的分布式治理機制。

我們希望更詳細地描述更改配置參數的第二種方式。

## 3. 創建配置提案

一個新的**配置提案**包含以下數據：
- 要更改的配置參數的索引
- 配置參數的新值（如果要刪除，則為Null）
- 提案到期的Unix時間
- 表示提案是否為**關鍵**的標誌
- 可選的**舊值哈希**，帶有當前值的單元哈希（僅當當前值具有指示哈希時，才能激活提案）

在主鏈中具有錢包的任何人都可以創建新的配置提案，前提是支付適當的費用。但是，只有驗證器才能投票贊成或反對現有的配置提案。

請注意，有**關鍵**和**普通**的配置提案。關鍵配置提案可以更改任何配置參數，包括所謂的關鍵配置參數之一（關鍵配置參數的列表存儲在配置參數`＃10`中，它本身是關鍵的）。但是，創建關鍵配置提案更加昂貴，通常需要在更多的回合中收集更多的驗證器投票（普通配置提案和關鍵配置提案的具體投票要求存儲在關鍵配置參數`＃11`中）。另

要創建一個新的配置提案，首先必須生成包含建議的新值的BoC（cell包）文件。具體方法取決於正在更改的配置參數。例如，如果我們想創建一個包含UTF-8字符串“TEST”（即`0x54455354`）的參數`-239`，我們可以按以下方式創建`config-param-239.boc`：調用Fift，然後輸入以下內容：


    <b "TEST" $, b> 2 boc+>B "config-param-239.boc" B>file
    bye

結果，將創建一個21字節的文件`config-param-239.boc`，其中包含所需值的序列化。

對於更複雜的情況，尤其是對於具有非負索引的配置參數，這種簡單的方法不易應用。我們建議使用`create-state`（在構建目錄中可用作`crypto/create-state`）代替`fift`，並複製並編輯源文件`crypto/smartcont/gen-zerostate.fif`和`crypto/smartcont/CreateState.fif`的適當部分，這些文件通常用於創建TON Blockchain的零狀態（對應於其他區塊鏈架構的“創世塊”）。

例如，考慮配置參數`#8`，其中包含當前啟用的全局區塊鏈版本和功能：


    capabilities#c4 version:uint32 capabilities:uint64 = GlobalVersion;
    _ GlobalVersion = ConfigParam 8;

我們可以通過運行lite client並輸入“getconfig 8”來檢查其當前值：

```
> getconfig 8
...
ConfigParam(8) = (
  (capabilities version:1 capabilities:6))

x{C4000000010000000000000006}
```

現在假設我們要啟用由位`#3`（`+8`）表示的功能，即`capReportVersion`（啟用時，此功能會強制所有收集者在它們生成的塊標題中報告其支持的版本和功能）。因此，我們希望擁有`version=1`和`capabilities=14`。在這個例子中，我們仍然可以猜測正確的序列化並直接在Fift中創建BoC文件。

    x{C400000001000000000000000E} s>c 2 boc+>B "config-param8.boc" B>file

結果，將創建一個30字節的文件`config-param8.boc`，其中包含所需的值。

但是，在更複雜的情況下，這可能不是一個選擇，因此我們可以以不同的方式執行此示例。即，我們可以查看源文件`crypto/smartcont/gen-zerostate.fif`和`crypto/smartcont/CreateState.fif`的相關部分。

    // version capabilities --
    { <b x{c4} s, rot 32 u, swap 64 u, b> 8 config! } : config.version!
    1 constant capIhr
    2 constant capCreateStats
    4 constant capBounceMsgBody
    8 constant capReportVersion
    16 constant capSplitMergeTransactions

and

    // version capabilities
    1 capCreateStats capBounceMsgBody or capReportVersion or config.version!

我們發現`config.version!`去掉最後的`8 config!`基本上就是我們需要的，因此我們可以創建一個臨時的Fift腳本，例如`create-param8.fif`:

```
#!/usr/bin/fift -s
"TonUtil.fif" include

1 constant capIhr
2 constant capCreateStats
4 constant capBounceMsgBody
8 constant capReportVersion
16 constant capSplitMergeTransactions
{ <b x{c4} s, rot 32 u, swap 64 u, b> } : prepare-param8

// create new value for config param #8
1 capCreateStats capBounceMsgBody or capReportVersion or prepare-param8
// check the validity of this value
dup 8 is-valid-config? not abort"not a valid value for chosen configuration parameter"
// print
dup ."Serialized value = " <s csr.
// save into file provided as first command line argument
2 boc+>B $1 tuck B>file
."(Saved into file " type .")" cr
```

現在，如果我們運行`fift -s create-param8.fif config-param8.boc`或者更好的是`crypto/create-state -s create-param8.fif config-param8.boc`(從構建目錄)，我們將看到以下輸出：

    Serialized value = x{C400000001000000000000000E}
    (Saved into file config-param8.boc)

然後，我們將獲得一個30字節的文件`config-param8.boc`，其內容與以前相同。

一旦我們有了所需配置參數值的文件，我們調用`crypto/smartcont`目錄中可以找到的腳本`create-config-proposal.fif`，並使用適當的參數。同樣，我們建議使用`create-state`（從構建目錄中可用的`crypto/create-state`）而不是`fift`，因為它是一個特殊的擴展版本的Fift，能夠進行更多與區塊鏈相關的有效性檢查：


```
$ crypto/create-state -s create-config-proposal.fif 8 config-param8.boc -x 1100000


Loading new value of configuration parameter 8 from file config-param8.boc
x{C400000001000000000000000E}

Non-critical configuration proposal will expire at 1586779536 (in 1100000 seconds)
Query id is 6810441749056454664 
resulting internal message body: x{6E5650525E838CB0000000085E9455904_}
 x{F300000008A_}
  x{C400000001000000000000000E}

B5EE9C7241010301002C0001216E5650525E838CB0000000085E9455904001010BF300000008A002001AC400000001000000000000000ECD441C3C
(a total of 104 data bits, 0 cell references -> 59 BoC data bytes)
(Saved to file config-msg-body.boc)
```

我們已經獲得了一個內部消息的主體，該消息需要從任何（錢包）智能合約發送到主鏈中的配置智能合約，其中包含適當數量的Toncoin。可以通過在Lite Client中輸入`getconfig 0`來獲取配置智能合約的地址：

```
> getconfig 0
ConfigParam(0) = ( config_addr:x5555555555555555555555555555555555555555555555555555555555555555)
x{5555555555555555555555555555555555555555555555555555555555555555}
```
我們已經獲得了一個內部消息的主體，該消息需要從任何（錢包）智能合約發送到主鏈中的配置智能合約，其中包含適當數量的Toncoin。可以通過在Lite Client中輸入`getconfig 0`來獲取配置智能合約的地址：

```
> runmethod -1:5555555555555555555555555555555555555555555555555555555555555555 proposal_storage_price 0 1100000 104 0

arguments:  [ 0 1100000 104 0 75077 ] 
result:  [ 2340800000 ] 
remote result (not to be trusted):  [ 2340800000 ] 
```

`proposal_storage_price`方法的參數是臨界標誌（此處為0），此提議將處於活動狀態的時間間隔（1.1百萬秒），數據中的位（104）和單元引用（0）的總數。最後兩個數量可以在`create-config-proposal.fif`的輸出中看到。

我们可以看到，创建此提议需要支付2.3408个Toncoin。最好在消息中添加至少1.5个Toncoin以支付處理費用，因此我們將在請求中一起發送4個Toncoin（所有多餘的Toncoin將被退還）。現在，我們使用`wallet.fif`（或我們使用的錢包對應的Fift腳本）從我們的錢包創建一個轉賬到配置智能合約，攜帶4個Toncoin和`config-msg-body.boc`的主體。這通常看起來像：

```
$ fift -s wallet.fif my-wallet -1:5555555555555555555555555555555555555555555555555555555555555555 31 4. -B config-msg-body.boc

Transferring GR$4. to account kf9VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVQft = -1:5555555555555555555555555555555555555555555555555555555555555555 seqno=0x1c bounce=-1 
Body of transfer message is x{6E5650525E835154000000085E9293944_}
 x{F300000008A_}
  x{C400000001000000000000000E}

signing message: x{0000001C03}
 x{627FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA773594000000000000000000000000000006E5650525E835154000000085E9293944_}
  x{F300000008A_}
   x{C400000001000000000000000E}

resulting external message: x{89FE000000000000000000000000000000000000000000000000000000000000000007F0BAA08B4161640FF1F5AA5A748E480AFD16871E0A089F0F017826CDC368C118653B6B0CEBF7D3FA610A798D66522AD0F756DAEECE37394617E876EFB64E9800000000E01C_}
 x{627FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA773594000000000000000000000000000006E5650525E835154000000085E9293944_}
  x{F300000008A_}
   x{C400000001000000000000000E}

B5EE9C724101040100CB0001CF89FE000000000000000000000000000000000000000000000000000000000000000007F0BAA08B4161640FF1F5AA5A748E480AFD16871E0A089F0F017826CDC368C118653B6B0CEBF7D3FA610A798D66522AD0F756DAEECE37394617E876EFB64E9800000000E01C010189627FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA773594000000000000000000000000000006E5650525E835154000000085E9293944002010BF300000008A003001AC400000001000000000000000EE1F80CD3
(Saved to file wallet-query.boc)
```

現在我們可以利用Lite Client將外部消息`wallet-query.boc`發送到區塊鏈上。

    > sendfile wallet-query.boc
    ....
    external message status is 1

等待一段時間後，我們可以檢查我們錢包的傳入消息，檢查是否有來自配置智能合約的回復消息，或者如果我們感到幸運，可以通過配置智能合約的`list_proposals`方法檢查所有有效的配置提案列表。

```
> runmethod -1:5555555555555555555555555555555555555555555555555555555555555555 list_proposals
...
arguments:  [ 107394 ] 
result:  [ ([64654898543692093106630260209820256598623953458404398631153796624848083036321 [1586779536 0 [8 C{FDCD887EAF7ACB51DA592348E322BBC0BD3F40F9A801CB6792EFF655A7F43BBC} -1] 112474791597373109254579258586921297140142226044620228506108869216416853782998 () 864691128455135209 3 0 0]]) ] 
remote result (not to be trusted):  [ ([64654898543692093106630260209820256598623953458404398631153796624848083036321 [1586779536 0 [8 C{FDCD887EAF7ACB51DA592348E322BBC0BD3F40F9A801CB6792EFF655A7F43BBC} -1] 112474791597373109254579258586921297140142226044620228506108869216416853782998 () 864691128455135209 3 0 0]]) ] 
... caching cell FDCD887EAF7ACB51DA592348E322BBC0BD3F40F9A801CB6792EFF655A7F43BBC
```

我們可以看到所有有效的配置提案列表只有一個條目，由一對值表示。

```
[6465...6321 [1586779536 0 [8 C{FDCD...} -1] 1124...2998 () 8646...209 3 0 0]]
```
第一個數字`6465..6321`是配置提案的唯一標識符，等於其256位哈希值。此對的第二個組件是描述此配置提案狀態的Tuple。此Tuple的第一個組件是配置提案的過期Unix時間（`1586779546`）。第二個組件（`0`）是臨界性標誌。接下來是配置提案本身，由三元組`[8 C {FDCD...} -1]`描述，其中`8`是要修改的配置參數的索引，`C {FDCD...}`是具有新值的單元格（由此單元格的哈希表示），而`-1`是此參數舊值的可選哈希（`-1`表示未指定此哈希）。 接下來，我們會看到一個大數字`1124...2998`，表示當前驗證器集的標識符，然後是一個空列表`()`, 代表迄今為止已經為此提案投票的所有當前活躍的驗證器集，然後是`weight_remaining`等於`8646...209` - 如果該提案尚未在本輪中收集足夠的驗證器投票，那麼這個數字是正數，否則為負數。然後我們會看到三個數字：`3 0 0`。這些數字是`rounds_remaining`（此提案最多存活三輪，即當前驗證器集的更改次數），`wins`（該提案收集了超過全體驗證器權重3/4投票的回合數），以及`losses`（該提案未能收集3/4的全體驗證器投票的回合數）。


我們可以通過要求lite-client使用其哈希`FDCD...`或足夠長的哈希前綴來擴展單元`C {FDCD ...}`，以檢查配置參數`＃8`的建議值：

```
> dumpcell FDC
C{FDCD887EAF7ACB51DA592348E322BBC0BD3F40F9A801CB6792EFF655A7F43BBC} =
  x{C400000001000000000000000E}
```
我們可以看到，該值為`x {C400000001000000000000000E}`，確實是我們嵌入到我們的配置建議中的值。 我們甚至可以要求lite-client將此單元顯示為TL-B類型的值（`ConfigParam 8`）。

```
> dumpcellas ConfigParam8 FDC
dumping cells as values of TLB type (ConfigParam 8)
C{FDCD887EAF7ACB51DA592348E322BBC0BD3F40F9A801CB6792EFF655A7F43BBC} =
  x{C400000001000000000000000E}
(
    (capabilities version:1 capabilities:14))
```
當考慮其他人創建的配置建議時，這尤其有用。

請注意，從現在開始，配置建議由其256位哈希標識--巨大的十進制數字`6465...6321`標識。 我們可以通過使用等於配置建議標識符的唯一參數運行get-method `get_proposal`，以檢查特定配置建議的當前狀態：

```
> runmethod -1:5555555555555555555555555555555555555555555555555555555555555555 get_proposal 64654898543692093106630260209820256598623953458404398631153796624848083036321
...
arguments:  [ 64654898543692093106630260209820256598623953458404398631153796624848083036321 94347 ] 
result:  [ [1586779536 0 [8 C{FDCD887EAF7ACB51DA592348E322BBC0BD3F40F9A801CB6792EFF655A7F43BBC} -1] 112474791597373109254579258586921297140142226044620228506108869216416853782998 () 864691128455135209 3 0 0] ] 
```
我們基本上獲得了與以前相同的結果，但僅限於一個配置建議，並且沒有配置建議的標識符在開頭。

## 4.投票支持配置建議

一旦創建了配置建議，它應該收集來自當前輪次中超過3/4的所有當前驗證器（按權重計，即按權益計）的投票，並且可能在幾個後續輪次（當選驗證器集）中收集投票。 這樣，必須經過一個顯著的多數來決定是否更改配置參數，這種多數不僅是當前一組驗證器的多數，還是幾個後續驗證器組的多數。

僅對於當前驗證器（在配置參數`＃34`中列出其永久公鑰）才能為配置建議投票。 過程大致如下：

- 驗證器的操作員在配置參數`＃34`中查找其驗證器在當前驗證器集合中的（基於零）索引`val-idx`。
- 運營商調用源樹目錄`crypto / smartcont`中找到的特殊Fift腳本`config-proposal-vote-req.fif`，將`val-idx`和`config-proposal-id`作為其參數：
```
    $ fift -s config-proposal-vote-req.fif -i 0 64654898543692093106630260209820256598623953458404398631153796624848083036321
    Creating a request to vote for configuration proposal 0x8ef1603180dad5b599fa854806991a7aa9f280dbdb81d67ce1bedff9d66128a1 on behalf of validator with index 0 
    566F744500008EF1603180DAD5B599FA854806991A7AA9F280DBDB81D67CE1BEDFF9D66128A1
    Vm90RQAAjvFgMYDa1bWZ-oVIBpkaeqnygNvbgdZ84b7f-dZhKKE=
    Saved to file validator-to-sign.req
```
- 然後，必須使用`validator-engine-console`中的`sign <validator-key-id> 566F744 ... 28A1`使用當前驗證器的私鑰對投票請求進行簽名，該請求已連接到驗證器。 這個過程與[Validator-HOWTO](https://toncoin.org/#/howto/validator)中描述的參與驗證器選舉的過程類似，但是這次必須使用當前活動密鑰。
- 接下來，必須調用另一個腳本`config-proposal-signed.fif`。 它具有與`config-proposal-req.fif`相似的參數，但它期望兩個額外的參數：用於簽署投票請求的公鑰的base64表示形式，以及簽名本身的base64表示形式。 再次，這與[Validator-HOWTO](https://toncoin.org/#/howto/validator)中描述的過程非常相似。
- 這樣，將創建包含內部消息主體的已簽名投票的文件`vote-msg-body.boc`，該內部消息攜帶著此配置提案。
- 然後，`vote-msg-body.boc`必須從任何位於主鏈中的智能合約（通常使用驗證器的控制智能合約）攜帶內部消息，並攜帶少量Toncoin進行處理（通常1.5 Toncoin足以滿足）。 這再次完全類似於驗證器選舉期間使用的程序。 通常通過運行實現：
```
$ fift -s wallet.fif my_wallet_id -1:5555555555555555555555555555555555555555555555555555555555555555 1 1.5 -B vote-msg-body.boc
```
（如果使用簡單的錢包來控制驗證器）然後從輕量級客戶端發送生成的文件`wallet-query.boc`：

```
> sendfile wallet-query.boc
```

您可以通過監視來自配置智能合約到控制智能合約的答案消息，了解投票請求的狀態。 或者，您可以通過配置智能合約的get-method`show_proposal`檢查配置提案的狀態：

```
> runmethod -1:5555555555555555555555555555555555555555555555555555555555555555 get_proposal 64654898543692093106630260209820256598623953458404398631153796624848083036321
...
arguments:  [ 64654898543692093106630260209820256598623953458404398631153796624848083036321 94347 ] 
result:  [ [1586779536 0 [8 C{FDCD887EAF7ACB51DA592348E322BBC0BD3F40F9A801CB6792EFF655A7F43BBC} -1] 112474791597373109254579258586921297140142226044620228506108869216416853782998 (0) 864691128455135209 3 0 0] ]
```
此時，投票此配置提案的驗證器索引列表應該不為空，並且應該包含您的驗證器的索引。在這個例子中，這個列表是（`0`），這意味著只有配置參數`#34`中索引為`0`的驗證器投票了。如果列表變得足夠大，那麼提案狀態中的倒數第二個整數（`3 0 0`中的第一個零）將增加一，表示此提案的新獲勝。如果獲勝次數大於或等於配置參數`#11`中指定的值，則自動接受配置提案，所提出的更改立即生效。另一方面，當驗證器集合發生變化時，已經投票的驗證器列表將變為空，`rounds_remaining`的值（`3 0 0`中的三）將減少一，如果它變為負數，則配置提案將被銷毀。如果它沒有被銷毀，並且在此輪中沒有贏得勝利，那麼失敗次數（`3 0 0`中的第二個零）將增加。如果它變得大於配置參數`#11`中指定的值，那麼配置提案將被丟棄。結果，所有沒有投票的驗證器都隱含地投票反對。


## 5. A自動化的投票方式來投票關於配置提案的決議

與`validator-engine-console`中的`createelectionbid`命令提供的自動化類似，`validator-engine`和`validator-engine-console`提供了一種自動執行前一節中大多數步驟的方法，可以產生一個`vote-msg-body.boc`，準備好與控制錢包一起使用。要使用此方法，必須將Fift腳本`config-proposal-vote-req.fif`和`config-proposal-vote-signed.fif`安裝到與validator-engine使用的相同目錄中，以查找`validator-elect-req.fif`和`validator-elect-signed.fif`，如[Validator-HOWTO](https://toncoin.org/#/howto/validator)第5節所述。之後，只需運行：

```
    createproposalvote 64654898543692093106630260209820256598623953458404398631153796624848083036321 vote-msg-body.boc
```
在validator-engine-console中使用以下命令創建`vote-msg-body.boc`，其中包含要發送到配置智能合約的內部消息的正文。

## 6. 升級配置智能合約和選民智能合約的代碼


有時候配置智能合約本身的代碼或選民智能合約的代碼必須升級。為此，使用與上述相同的機制。新代碼將存儲在僅有的值單元的唯一引用中，並將該值單元作為新值提議給配置參數`-1000`（用於升級配置智能合約）或`-1001`（用於升級選民智能合約）。這些參數被認為是關鍵的，因此需要很多驗證器投票才能更改配置智能合約（這類似於採用新憲法）。我們期望這樣的更改將首先在測試網絡中進行測試，在每個驗證器運營商決定投票贊成或反對建議更改之前在公共論壇中討論建議的更改。


或者，關鍵的配置參數`0`（配置智能合約的地址）或`1`（選民智能合約的地址）可以更改為其他值，這些值必須對應於已經存在並且已經正確初始化的智能合約。特別是，新的配置智能合約必須在其持久數據的第一個引用中包含一個有效的配置字典。由於在不同的智能合約之間正確轉移變更數據（例如活動配置提案列表，或驗證器選舉的先前和當前參與者列表）並不容易，因此在大多數情況下最好升級現有智能合約的代碼而不是更改配置智能合約地址。

有兩個輔助腳本用於創建此類配置提案以升級配置或選民智能合約的代碼。即，`create-config-upgrade-proposal.fif`加載一個Fift彙編器源文件（默認情況下為`auto/config-code.fif`，對應於由FunC編譯器自`crypto/smartcont/config-code.fc`自動生成的代碼），並創建相應的配置提案（對於配置參數`-1000`）。同樣，`create-elector-upgrade-proposal.fif`加載一個Fift彙編器源文件（默認情況下為`auto/elector-code.fif`），並使用它創建配置參數`-1001`的配置提案。通過這種方式，創建升級這兩個智能合約之一的配置提案應該非常簡單。但是，還應發布智能合約的修改FunC源代碼以及用於編譯它的FunC編譯器的確切版本，以便所有驗證器（或更確切地說是它們的操作者）都能夠在配置提案中重現代碼（並比較哈希），並在決定投票贊成或反對建議更改之前研究和討論源代碼和對代碼的更改。

