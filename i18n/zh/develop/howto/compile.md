# 從原始碼編譯

:::caution
本節介紹與 TON 進行低級交互的說明和手冊。
:::

## 通用

該軟件可能會在大多數 Linux 系統上正常編譯和運行。它應該可以在 macOS 甚至 Windows 上運行。

1) 從 GitHub 存儲庫 https://github.com/ton-blockchain/ton/ 下載最新版本的 TON 區塊鏈源代碼：

```bash
git clone --recurse-submodules https://github.com/ton-blockchain/ton.git
```

2) 安裝最新版本的:
   - `make`
   - `cmake` 版本 3.0.2 或更高版本
   - `g++` 或 `clang`（或適用於您的操作系統的其他 C++14 兼容編譯器）。
   - OpenSSL（包括 C 標頭文件）版本 1.1.1 或更高版本
   - `build-essential`，`zlib1g-dev`，`gperf`，`libreadline-dev`，`ccache`，`libmicrohttpd-dev`

   在 Ubuntu 上:


```bash
apt update
sudo apt install build-essential cmake clang openssl libssl-dev zlib1g-dev gperf libreadline-dev ccache libmicrohttpd-dev
```


3) 假設你已經將源代碼樹抓取到目錄 `~/ton`，其中 `~` 是你的家目錄，並創建了一個空目錄 `~/ton-build`：

```bash
mkdir ton-build
```

然後在 Linux 或 MacOS 的終端中運行以下命令：

```bash
cd ton-build
export CC=clang
export CXX=clang++
cmake -DCMAKE_BUILD_TYPE=Release ../ton && cmake --build . -j$(nproc)
```

:::warning
在進行下一步之前，如果您的MacOS是Intel處理器，我們可能需要使用`brew`安裝`openssl@3`或只需連接庫：

```zsh
brew install openssl@3
```

Then need to inspect `/usr/local/opt`:

```zsh
ls /usr/local/opt
```

找到`openssl@3`庫並導出本地變量：


```zsh
export OPENSSL_ROOT_DIR=/usr/local/opt/openssl@3
```

:::

:::tip
如果您正在低內存（例如，1 Gb）的計算機上編譯，不要忘記[創建交換分區](/develop/howto/compile-swap)。
:::

## 下載全局配置

對於像lite client這樣的工具，您需要下載全局網絡配置。

從https://ton-blockchain.github.io/global.config.json下載最新的配置文件，以供主網使用：


```bash
wget https://ton-blockchain.github.io/global.config.json
```

或從https://ton-blockchain.github.io/testnet-global.config.json為測試網構建：


```bash
wget https://ton-blockchain.github.io/testnet-global.config.json
```

## Lite Client

要構建lite client，請完成[共同部分](/develop/howto/compile#common)，[下載配置](/develop/howto/compile#download-global-config)，然後執行以下步驟：


```bash
cmake --build . --target lite-client
```

使用配置運行Lite Client：


```bash
./lite-client/lite-client -C global.config.json
```

如果一切都成功安裝，Lite Client將連接到一個特殊的服務器（TON區塊鏈網絡的完整節點），並向該服務器發送一些查詢。
如果您將一個可寫的“數據庫”目錄作為客戶端的額外參數指定，它將下載並保存與最新的主鏈塊相對應的塊和狀態：


```bash
./lite-client/lite-client -C global.config.json -D ~/ton-db-dir
```

要獲取Lite Client的基本幫助信息，請在Lite Client中輸入“help”。輸入“quit”或按“Ctrl-C”退出。

## FunC

要從源代碼構建FunC編譯器，請完成上面描述的[共同部分](/develop/howto/compile#common)，然後執行以下步驟：


```bash
cmake --build . --target func
```

要編譯FunC智能合約：

```bash
func -o output.fif -SPA source0.fc source1.fc ...
```

## Fift

要從源代碼構建Fift編譯器，請完成上面描述的[共同部分](/develop/howto/compile#common)，然後執行以下步驟：


```bash
cmake --build . --target fift
```

要運行Fift腳本：


```bash
fift -s script.fif script_param0 script_param1 ..
```

## Tonlib-cli

要構建tonlib-cli，請完成[共同部分](/develop/howto/compile#common)，[下載配置](/develop/howto/compile#download-global-config)，然後執行以下步驟：

```bash
cmake --build . --target tonlib-cli
```

使用配置運行tonlib-cli：


```bash
./tonlib/tonlib-cli -C global.config.json
```

要獲取tonlib-cli的基本幫助信息，請在tonlib-cli中輸入“help”。輸入“quit”或按“Ctrl-C”退出。

## RLDP-HTTP-Proxy

要構建rldp-http-proxy，請完成[共同部分](/develop/howto/compile#common)，[下載配置](/develop/howto/compile#download-global-config)，然後執行以下步驟：


```bash
cmake --build . --target rldp-http-proxy
```

代理二進制文件將位於：

```bash
rldp-http-proxy/rldp-http-proxy
```

## generate-random-id

要構建generate-random-id，請完成[共同部分](/develop/howto/compile#common)，然後執行以下步驟：


```bash
cmake --build . --target generate-random-id
```

The binary will be located as:

```bash
utils/generate-random-id
```

## storage-daemon

要構建storage-daemon和storage-daemon-cli，請完成[共同部分](/develop/howto/compile#common)，然後執行以下步驟：


:::tip
Currently storage-daemon located at `testnet` branch, so you need type `git checkout testnet` after cloning the repo.
:::

```bash
cmake --build . --target storage-daemon storage-daemon-cli
```

二進制文件將位於：


```bash
storage/storage-daemon/
```

# 編譯舊版的TON

TON發布版本：https://github.com/ton-blockchain/ton/tags


```bash
git clone https://github.com/ton-blockchain/ton.git
cd ton
# git checkout <TAG> for example checkout func-0.2.0
git checkout func-0.2.0
git submodule update --init --recursive 
cd ..
mkdir ton-build
cd ton-build
cmake ../ton
# build func 0.2.0
cmake --build . --target func
```

## 在 Apple M1 上編譯舊版本：

TON從2022年6月11日開始支持Apple M1（[添加Apple M1支持（# 401）](https://github.com/ton-blockchain/ton/blob/c00302ced4bc4bf1ee0efd672e7c91e457652430)提交）。

要在Apple M1上編譯較舊的TON版本：

1. 將RocksDb子模塊更新為6.27.3

   ```bash
   cd ton/third-party/rocksdb/
   git checkout fcf3d75f3f022a6a55ff1222d6b06f8518d38c7c
   ```

2. 用https://github.com/ton-blockchain/ton/blob/c00302ced4bc4bf1ee0efd672e7c91e457652430/CMakeLists.txt替換根目錄下的`CMakeLists.txt`文件

