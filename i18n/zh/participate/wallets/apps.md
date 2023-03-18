# Wallet Apps (for Devs)

## Overview

This article describes wallets from a developmental perspective. The end goal  is to create wallet applications that support TON mass adoption.

If you want to find a wallet to install, open [ton.org/wallets](https://ton.org/wallets).

## Non-custodial wallets

:::info
With a non-custodial wallet, the user owns the wallet and holds its private key by themself.
:::

* [TON Wallet](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd) — one of the first wallets in the TON ecosystem developed by TON Foundation.
* [Tonkeeper](https://tonkeeper.com/) — is an alternative wallet, that is a favourite among users today.
* [Tonhub](https://tonhub.com/) — is another rapidly developing wallet with advanced features (TON Whales Staking UI).
* [OpenMask](https://www.openmask.app/) — an open-source browser extension wallet with biometric authentication.
* [MyTonWallet](https://mytonwallet.io/) — is the most full-featured web wallet and browser extension for TON.


### Basics features
| Wallet     | Jetton & NFT transfers        | Ton Connect 2.0                                                         | Authorization                                               | Wallet contract                                                                                               |
|------------|-----------------|-------------------------------------------------------------------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| TON Wallet | Not implemented | -                                                                       | -                                                           | [wallet v3](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc)               |
| Tonkeeper  | Supported       | [Supported](https://github.com/ton-society/ton-footsteps/issues/161)    | [TON Connect 2.0](/develop/dapps/ton-connect)               | [wallet v4](https://github.com/ton-blockchain/wallet-contract/tree/3fd1d7ae39f1c46ec1f2be54c4040d8d87505e0f)  |
| Tonhub     | Supported*        | [In progress](https://github.com/ton-society/ton-footsteps/issues/108 ) | [tonhub connector](https://developers.tonhub.com/docs/apps) | [wallet v4](https://github.com/ton-blockchain/wallet-contract/tree/3fd1d7ae39f1c46ec1f2be54c4040d8d87505e0f)  |
| OpenMask   | Supported       | [Supported](https://github.com/ton-society/ton-footsteps/issues/107)    | [TON Connect 2.0](/develop/dapps/ton-connect)               | [wallet v4](https://github.com/ton-blockchain/wallet-contract/tree/3fd1d7ae39f1c46ec1f2be54c4040d8d87505e0f)  |
| MyTonWallet| Supported | [Supported](https://github.com/ton-society/ton-footsteps/issues/149)    | [TON Connect 2.0](/develop/dapps/ton-connect)               | [wallet v4](https://github.com/ton-blockchain/wallet-contract/tree/3fd1d7ae39f1c46ec1f2be54c4040d8d87505e0f) |


> *Tonhub extension opens a built-in browser which allows for NFT market placements. Jetton is full supported.


### TON Wallet

TON Wallet was the first step in mass-adoption blockchain technology available to ordinary users. It demonstrates how a wallet must works on TON Blockchain.

|                                            |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;![TON wallet](/img/docs/wallet-apps/TonWallet.png?raw=true) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | 


#### Pros and Cons
- ✅ The original wallet developed by TON Foundation. TON Wallet works according to the vision of TON Blockchain's core developers.
- ✅ Multi-platform architecture support. It works in Linux, Windows, MacOS, iOS, Android and as well as a Chrome plugin.
- ✅ [Bug bounty program](https://github.com/ton-blockchain/bug-bounty)
- ❌ Rare updates. This wallet does not have not all up-to-date features (TON DNS address, wallet-v4 contract not supported).
- ❌ The current UI is outdated and is worse than alternative wallets.

#### Ton wallet test environment

To switch Ton classic wallet to test environment, you should to open in browser with testnet parameter:

#### Links
- [Github*](https://github.com/ton-blockchain/wallet-ios)

  > *TON Wallet clients for every supported OS placed in nearby repositories.

### Tonkeeper

[Tonkeeper](https://tonkeeper.com/) - is the most downloaded wallet, developed by the Tonkeeper team and has active support from both users and developers.

|                                               |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;![Tonkeeper](/img/docs/wallet-apps/Tonkeeper.png?raw=true) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | 


#### Pros and Cons
- ✅ This app is most popular with users.
- ✅ Supports all up-to-date features including native NFT transfer between user wallets.
- ❌ Tonkeeper is only supported by mobile iOS and Android platforms.
- ❌ To contribute requires advanced skills. A lot of the job already done and it will be hard for newcomers to add something significant.

#### Tonkeeper test environment


To switch Tonkeeper application between Mainnet and Testnet: open settings, at the bottom of the settings screen tap 5 times on the Tonkeeper icon and switch net in the dev menu.

|                                                      |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;![TestMode](/img/docs/wallet-apps/Tonkeeper-testnet.png?raw=true) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | 



#### Links
- [Github](https://github.com/tonkeeper/wallet)
- [Tonkeeper Wallet API](https://github.com/tonkeeper/wallet-api)




### Tonhub

[Tonhub](https://tonhub.com/) - is another fully-fledged TON wallet, that has basic up-to-date features support. Ton Whales are rapidly increasing the capabilities of the wallet.

|                                    |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;![Tonhub](/img/docs/wallet-apps/Tonhub.png?raw=true) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | 


#### Pros and Cons

- ✅ Has own custom [Ton Nominator](https://github.com/tonwhales/ton-nominators) contract supported with Tonhub UI.
- ✅ Open-sourced wallet from the beginning of the existing application.
- ✅ [Bug-bounty program](https://tonwhales.com/bounty).
- ❌ Have no support for all desktop platforms.
- ❌ To contribute requires advanced skills.

#### Tonhub test environment
For use in testnet necessary separate the application Sandbox.

#### Links
- [Github](https://github.com/tonwhales/wallet)
- [Sandbox iOS](https://apps.apple.com/app/ton-development-wallet/id1607857373)
- [Sandbox Android](https://play.google.com/store/apps/details?id=com.tonhub.wallet.testnet)


### OpenMask

[OpenMask](https://www.openmask.app/) - is the trailblazing tool enabling user interactions and experience on Web3 as browser extension.

|                                                                |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;![OpenMask](/img/docs/wallet-apps/OpenMask.png?raw=true) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |

#### Pros and Cons
- ✅ Convenient for developers environment to learn and create dApps via desktop without mobile devices.
- ✅ Unique functions such as multiple wallets, with detailed descriptions and examples in its documentation.
- ❌ Has almost no integration with dApps at the moment.
- ❌ Supports only browser extension platform.

#### OpenMask test environment
To switch OpenMask between Mainnet and Testnet: you need to click on "mainnet/testnet" button on the top of the OpenMask's main screen and chose network you need.

#### Links

- [GitHub](https://github.com/OpenProduct/openmask-extension)
- [Documentation](https://www.openmask.app/docs/introduction)

### MyTonWallet


[MyTonWallet](https://mytonwallet.io/) - is the most feature-rich web wallet and browser extension for TON – with support of tokens, NFT, TON DNS, TON Sites, TON Proxy, and TON Magic.


|                                                                                                                                                                                                                                   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;![MyTonWallet](/img/docs/wallet-apps/MyTonWallet.png?raw=true) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |




#### Pros and Cons
- ✅ Implemented all basic functions.
- ✅ Unique feature - management of the official [Nominator Pool contract](https://github.com/ton-blockchain/nominator-pool) from wallet UI.
- ❌ Supports only web browser and Chrome extension platform.

#### MyTonWallet test environment
To switch the MyTonWallet to Testnet: open Settings and by clicking 5 times on the app version open the network switcher.

#### Links

- [GitHub](https://github.com/mytonwalletorg/mytonwallet)
- [MyTonWallet Telegram](https://t.me/MyTonWalletRu)


## Custodial wallets

:::info
With a custodial wallet, user trusts somebody else to hold the wallet's private key.
:::

### @wallet

[@wallet](https://t.me/wallet) — bot application to send and receive or trade p2p TON inside Telegram. Supports Telegram Web App UI.


|                                                                                                                                                                                                                            |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;![wallet](/img/docs/wallet-apps/Wallet.png?raw=true) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |


### @cryptobot

[@cryptobot](https://t.me/cryptobot) — A Telegram bot wallet for storing, transferring and exchanging TON.


|                                                                                                                                                                                                                                 |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;![CryptoBot](/img/docs/wallet-apps/CryptoBot.png?raw=true) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |


#### Links for 3d-party integrations

- [Crypto Pay API](https://help.crypt.bot/crypto-pay-api)

### @tonRocketBot

[@tonRocketBot](https://t.me/tonRocketBot) - A Telegram bot wallet for storing, transferring and exchanging TON. Supports Jetton trading as well.


|                                                                                                                                                                                                                                        |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;![tonrocketbot](/img/docs/wallet-apps/tonrocketbot.png?raw=true) &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |


#### Links for 3d-party integrations

- [Rocket exchange](https://trade.ton-rocket.com/api/)
- [Rocket pay docs](https://pay.ton-rocket.com/api/)