# Using toncli

_toncli—The Open Network cross-platform smart contract command line interface._

Easy to deploy and interact with TON smart contracts.

Good solution for **Python** stack developers.

* [GitHub repository](https://github.com/disintar/toncli)

## Quick Start 📌

Here are tutorials made using a toncli library:
* [Quick start guide](https://github.com/disintar/toncli/blob/master/docs/quick_start_guide.md)—simple steps for deploying an example smart contract to TON.
* [TON Learn: FunC journey overview. Part 1](https://blog.ton.org/func-journey)
* [TON Learn: FunC journey overview. Part 2](https://blog.ton.org/func-journey-2)
* [TON Learn: FunC journey overview. Part 3](https://blog.ton.org/func-journey-3)
* [TON Learn: 10 zero-to-hero lessons](https://github.com/romanovichim/TonFunClessons_Eng) ([Ru version](https://github.com/romanovichim/TonFunClessons_ru))

## Installation 💾

### Docker: linux / macOS (m1 supported) 

* Docker-hub pre-build images can be founded [here](https://hub.docker.com/r/trinketer22/func_docker/)
* Docker files with instructions can be founded [here](https://github.com/Trinketer22/func_docker)

### Linux / macOS (intel)

1) Download the necessary special pre-builds (use the latest build)
* for Linux: [here](https://github.com/SpyCheese/ton/actions/workflows/ubuntu-compile.yml?query=branch%3Atoncli-local++)
* for Mac: [here](https://github.com/SpyCheese/ton/actions/workflows/macos-10.15-compile.yml?query=branch%3Atoncli-local)

:::info Download special pre-builds tip
To download the necessary files, you must log-in to your account
:::

2) Install [Python3.9](https://www.python.org/downloads/) or higher  

3) Run in terminal `pip install toncli` or `pip3 install toncli`

:::tip Possible error
If you see `WARNING: The script toncli is installed in '/Python/3.9/bin' which is not on PATH`, then add the full path to bin to the PATH env
:::

4) Run `toncli` and pass absolute path to `func/fift/lite-client` from first step


### Windows

1) Download the necessary special pre-builds from [here](https://github.com/SpyCheese/ton/actions/workflows/win-2019-compile.yml?query=branch%3Atoncli-local) (use the latest build)

:::info Download special pre-builds tip
To download the necessary files, you must log-in to your account
:::

2) Install [Python3.9](https://www.python.org/downloads/) or higher 

:::info Very important! 
During installation, on the first screen, you need to click the `Add Python to PATH` checkbox
:::

3)  Open the terminal as an administrator and `pip install toncli` by installing `toncli`

4) Unzip the downloaded archive and add [libcrypto-1_1-x64.dll](https://disk.yandex.ru/d/BJk7WPwr_JT0fw) to unziped files

5) Open the folder in the console for windows users: 

**Windows 11**:
* Right mouse button, open in the terminal 

**Windows 10**: 
* Copy the path in Explorer and run in Terminal `cd FULL PATH`

## Create a project ✏️ 

These are simple steps to deploy an example smart contract in TON.
You can read the official documentation [here](https://github.com/disintar/toncli/blob/master/docs/quick_start_guide.md)
### Step-by-step guide

1) Open the terminal as an administrator and go to your project folder

2) To create a project, run `toncli start YOUR-PROJECT-NAME`

3) Go to the project folder `cd YOUR-PROJECT-NAME`

:::info Result 
Toncli has created a simple wallet project, you can see 4 folders in it:
* build
* func
* fift
* test
:::

4) You can deploy it to testnet or mainnet: `toncli deploy -n testnet`

## Examples

Contributors have prepared sample projects very well covered by the new tests. For example, now two commands can be used to deploy an NFT collection or a Jetton.

```bash
toncli start nft_colletion/jetton_minter/nft_item/jetton_wallet
```

All of these projects have a lot of interesting examples of toncli and blockchain interaction, as well as extremely tests that will help in developing custom smart contracts.

## To test smart contracts using toncli, go to [testing](/develop/smart-contracts/testing/toncli)


## Useful articles

Other useful articles about using toncli in development:

1. [All cli commands](https://github.com/disintar/toncli/blob/master/docs/advanced/commands.md)
2. [Run get-methods](https://github.com/disintar/toncli/blob/master/docs/advanced/get_methods.md)
3. [Multiple contracts](https://github.com/disintar/toncli/blob/master/docs/advanced/multiple_contracts.md)
4. [Send boc with fift](https://github.com/disintar/toncli/blob/master/docs/advanced/send_boc_with_fift.md)
5. [Project structure](https://github.com/disintar/toncli/blob/master/docs/advanced/project_structure.md)
6. [Interesting features](https://github.com/disintar/toncli/blob/master/docs/advanced/intresting_features.md)
7. [Send internal fift messages](https://github.com/disintar/toncli/blob/master/docs/advanced/send_fift_internal.md)
8. [How does the FunC test work?](https://github.com/disintar/toncli/blob/master/docs/advanced/func_tests_new.md)
9. [How to debug transactions with toncli?](https://github.com/disintar/toncli/blob/master/docs/advanced/transaction_debug.md)
10. [Dockerfile for FunC testing GitHub repository](https://github.com/Trinketer22/func_docker)
