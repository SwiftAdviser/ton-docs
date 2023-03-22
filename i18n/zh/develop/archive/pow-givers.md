# POW Givers

:::warning 廢棄
此信息可能已過時，不再有用。可以忽略它。
:::


本文的目的是描述如何與工作量證明(PoW)的Giver智能合約互動以獲得TON Coin。我們假設您已熟悉TON區塊鏈輕客戶端（Lite Client），如在`入門`中所解釋的，以及編譯輕客戶端和其他軟件所需的程序。為了獲得運行驗證器所需的更多TON Coin，我們還假設您熟悉`完整節點（Full Node）`和`驗證器（Validator）`頁面。獲得更多TON Coin還需要一台足夠強大的專用服務器來運行完整節點。獲得少量TON Coin不需要專用服務器，可以在幾分鐘內在家用電腦上完成。


> 請注意，由於礦工數量眾多，目前任何挖礦都需要大量資源。


## 1. 工作量證明(PoW) Giver 智能合約

為了防止少數惡意方收集所有的TON Coin，一種特殊類型的"工作量證明(PoW) Giver"智能合約已被部署在網絡的主鏈上。這些智能合約的地址如下：

小型Giver（每隔幾分鐘發送10到100個TON Coin）：

* kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN
* kf8SYc83pm5JkGt0p3TQRkuiM58O9Cr3waUtR9OoFq716lN-
* kf-FV4QTxLl-7Ct3E6MqOtMt-RGXMxi27g4I645lw6MTWraV
* kf_NSzfDJI1A3rOM0GQm7xsoUXHTgmdhN5-OrGD8uwL2JMvQ
* kf8gf1PQy4u2kURl-Gz4LbS29eaN4sVdrVQkPO-JL80VhOe6
* kf8kO6K6Qh6YM4ddjRYYlvVAK7IgyW8Zet-4ZvNrVsmQ4EOF
* kf-P_TOdwcCh0AXHhBpICDMxStxHenWdLCDLNH5QcNpwMHJ8
* kf91o4NNTryJ-Cw3sDGt9OTiafmETdVFUMvylQdFPoOxIsLm
* kf9iWhwk9GwAXjtwKG-vN7rmXT3hLIT23RBY6KhVaynRrIK7
* kf8JfFUEJhhpRW80_jqD7zzQteH6EBHOzxiOhygRhBdt4z2N

大型Giver（每天至少發送10,000個TON Coin）：

* kf8guqdIbY6kpMykR8WFeVGbZcP2iuBagXfnQuq0rGrxgE04
* kf9CxReRyaGj0vpSH0gRZkOAitm_yDHvgiMGtmvG-ZTirrMC
* kf-WXA4CX4lqyVlN4qItlQSWPFIy00NvO2BAydgC4CTeIUme
* kf8yF4oXfIj7BZgkqXM6VsmDEgCqWVSKECO1pC0LXWl399Vx
* kf9nNY69S3_heBBSUtpHRhIzjjqY0ChugeqbWcQGtGj-gQxO
* kf_wUXx-l1Ehw0kfQRgFtWKO07B6WhSqcUQZNyh4Jmj8R4zL
* kf_6keW5RniwNQYeq3DNWGcohKOwI85p-V2MsPk4v23tyO3I
* kf_NSPpF4ZQ7mrPylwk-8XQQ1qFD5evLnx5_oZVNywzOjSfh
* kf-uNWj4JmTJefr7IfjBSYQhFbd3JqtQ6cxuNIsJqDQ8SiEA
* kf8mO4l6ZB_eaMn1OqjLRrrkiBcSt7kYTvJC_dzJLdpEDKxn

> 請注意，目前所有大型Giver都已耗盡。

前十個智能合約允許希望獲得少量TON Coin的用戶在不花費太多計算能力的情況下獲得一些（通常，家用電腦上幾分鐘的工作就足夠了）。其餘的智能合約用於獲得運行網絡驗證器所需的更多TON Coin；通常，在足夠運行驗證器的專用服務器上工作一天就足以獲得所需數量。


> 請注意，目前由於礦工數量眾多，挖掘小型Giver需要大量資源。

您應該隨機選擇其中一個"工作量證明Giver"智能合約（根據您的目的從這兩個列表中選擇一個），並通過類似於挖礦的過程從這個智能合約獲得TON Coin。本質上，您需要向所選的"工作量證明Giver"智能合約提交一個包含工作量證明和您錢包地址的外部消息，然後將向您發送所需金額。

## 2. 挖礦過程

為了創建一個包含"工作量證明"的外部消息，您應該運行一個特殊的挖礦實用程序，該實用程序是從位於GitHub存儲庫的TON源代碼編譯而來。該實用程序位於編譯目錄下的`./crypto/pow-miner`文件中，可以通過在編譯目錄中輸入`make pow-miner`來編譯。

然而，在運行 `pow-miner` 之前，您需要知道所選“工作量證明贈予者”智能合約的 `seed` 和 `complexity` 參數的實際值。這可以通過調用該智能合約的 get 方法 `get_pow_params` 來完成。例如，如果您使用贈予者智能合約 `kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN`，您可以簡單地輸入：


```
> runmethod kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN get_pow_params
```

在 Lite Client 控制台中輸入並獲取類似以下的輸出：

``` ...
    arguments:  [ 101616 ] 
    result:  [ 229760179690128740373110445116482216837 53919893334301279589334030174039261347274288845081144962207220498432 100000000000 256 ] 
    remote result (not to be trusted):  [ 229760179690128740373110445116482216837 53919893334301279589334030174039261347274288845081144962207220498432 100000000000 256 ]
```

「result:」行中的前兩個大數字是此智能合約的「seed」和「complexity」。在此示例中，seed 是 `229760179690128740373110445116482216837`，而 complexity 則為 `53919893334301279589334030174039261347274288845081144962207220498432`。

接下來，您將使用以下方式調用 `pow-miner` 工具：

```
$ crypto/pow-miner -vv -w<num-threads> -t<timeout-in-sec> <your-wallet-address> <seed> <complexity> <iterations> <pow-giver-address> <boc-filename>
```

在此：
* `<num-threads>` 是您希望用於挖礦的CPU核心數。
* `<timeout-in-sec>` 是礦工在承認失敗之前最多運行的秒數。
* `<your-wallet-address>` 是您的錢包地址（可能尚未初始化）。它可以在主鏈或工作鏈上（注意，您需要一個主鏈錢包才能控制驗證器）。
* `<seed>` 和 `<complexity>` 是通過運行get-method `get-pow-params`獲得的最新值。
* `<pow-giver-address>` 是所選工作量證明Giver智能合約的地址。
* `<boc-filename>` 是成功時將保存工作量證明的外部消息的輸出文件的文件名。

例如，如果您的錢包地址是 `kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7`，您可以運行：

```
$ crypto/pow-miner -vv -w7 -t100 kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7 229760179690128740373110445116482216837 53919893334301279589334030174039261347274288845081144962207220498432 100000000000 kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN mined.boc
```

程序將運行一段時間（在此例中最多100秒），然後成功終止（退出代碼為零）並將所需的工作量證明保存到文件`mined.boc`中，或者如果未找到工作量證明，則以非零退出代碼終止。

如果失敗，您將看到類似以下內容：

```
   [ expected required hashes for success: 2147483648 ]
   [ hashes computed: 1192230912 ]
```

程序將以非零退出代碼終止。然後，您必須再次獲得`seed`和`complexity`（因為在此期間，由於處理了更成功的礦工的請求，它們可能已經發生了變化），並使用新參數重新運行`pow-miner`，反覆執行過程，直至成功。

成功時，您將看到類似以下內容：

```
   [ expected required hashes for success: 2147483648 ]
   4D696E65005EFE49705690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1A1F533B3BC4F5664D6C743C1C5C74BB3342F3A7314364B3D0DA698E6C80C1EA4ACDA33755876665780BAE9BE8A4D6385A1F533B3BC4F5664D6C743C1C5C74BB3342F3A7314364B3D0DA698E6C80C1EA4
   Saving 176 bytes of serialized external message into file `mined.boc`
   [ hashes computed: 1122036095 ]
```

接下來，您可以使用Lite Client從文件'mined.boc'向工作量證明贈與者智能合約發送外部消息（您必須盡快進行此操作）：


```
> sendfile mined.boc
... external message status is 1
```

makefile
Copy code
你可以等待幾秒鐘，並檢查您錢包的狀態：

:::info
請注意，此處及以後的代碼、注釋和/或文檔可能包含“克”、“納克”等參數、方法和定義。這是Telegram開發的原始TON代碼的遺產。Gram加密貨幣從未發行。TON的貨幣是Toncoin，TON測試網的貨幣是Test Toncoin。
:::
```
> last
> getaccount kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7
...
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:0 address:x5690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:1)
      bits:(var_uint len:1 value:111)
      public_cells:(var_uint len:0 value:0)) last_paid:1593722498
    due_payment:nothing)
  storage:(account_storage last_trans_lt:7720869000002
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:5 value:100000000000))
      other:(extra_currencies
        dict:hme_empty))
    state:account_uninit))
x{C005690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F12025BC2F7F2341000001C169E9DCD0945D21DBA0004_}
last transaction lt = 7720869000001 hash = 83C15CDED025970FEF7521206E82D2396B462AADB962C7E1F4283D88A0FAB7D4
account balance is 100000000000ng
```

如果在您之前沒有人使用此種子(seed)和複雜度(complexity)發送了有效的工作證明，Proof-of-Work Giver將接受您的工作證明，並將其反映在您的錢包餘額上（在發送外部消息後可能會經過10或20秒，才會發生這種情況；請確保進行多次嘗試，每次在檢查錢包餘額之前輸入`last`以刷新Lite Client狀態）。如果成功，您將看到餘額已增加（甚至如果以前不存在，還會創建未初始化狀態的錢包）。如果失敗，您必須獲取新的`seed`和`complexity`，並從頭開始重複挖礦過程。

如果您運氣好，錢包餘額已增加，您可能希望在未初始化之前將錢包初始化（有關創建錢包的更多信息，請參見`逐步`）：


```
> sendfile new-wallet-query.boc
... external message status is 1
> last
> getaccount kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7
...
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:0 address:x5690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:3)
      bits:(var_uint len:2 value:1147)
      public_cells:(var_uint len:0 value:0)) last_paid:1593722691
    due_payment:nothing)
  storage:(account_storage last_trans_lt:7720945000002
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:5 value:99995640998))
      other:(extra_currencies
        dict:hme_empty))
    state:(account_active
      (
        split_depth:nothing
        special:nothing
        code:(just
          value:(raw@^Cell 
            x{}
             x{FF0020DD2082014C97BA218201339CBAB19C71B0ED44D0D31FD70BFFE304E0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54}
            ))
        data:(just
          value:(raw@^Cell 
            x{}
             x{00000001CE6A50A6E9467C32671667F8C00C5086FC8D62E5645652BED7A80DF634487715}
            ))
        library:hme_empty))))
x{C005690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1206811EC2F7F23A1800001C16B0BC790945D20D1929934_}
 x{FF0020DD2082014C97BA218201339CBAB19C71B0ED44D0D31FD70BFFE304E0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54}
 x{00000001CE6A50A6E9467C32671667F8C00C5086FC8D62E5645652BED7A80DF634487715}
last transaction lt = 7720945000001 hash = 73353151859661AB0202EA5D92FF409747F201D10F1E52BD0CBB93E1201676BF
account balance is 99995640998ng
```

The previous model used in this conversation is unavailable. We've switched you to the latest default model
markdown
Copy code
現在您是100 Toncoin的榮幸擁有者。恭喜！

## 3. 在失敗的情況下自動化挖礦過程

如果您長時間無法獲得Toncoin，可能是因為太多其他用戶同時從同一個Proof-of-Work Giver智能合約進行挖掘。也許您應該從上面提供的一個列表中選擇另一個Proof-of-Work Giver智能合約。或者，您可以編寫一個簡單的腳本，自動使用正確的參數一遍又一遍地運行`pow-miner`，直到成功（通過檢查`pow-miner`的退出代碼來檢測）並使用參數`-c 'sendfile mined.boc'`調用Lite Client，在找到外部消息後立即發送。