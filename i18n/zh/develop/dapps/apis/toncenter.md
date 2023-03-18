# TON Center API

_Standard HTTP JSON RPC. Similar to other blockchain APIs._

Clients connect to the [ton-http-api](https://github.com/toncenter/ton-http-api) server that proxies requests to the lite server (node) using TonLib.

You can connect to public [toncenter.com](https://toncenter.com) or run your own http-api instance.

## Pros & Cons

👍 — Habitual. Suitable for a quick start for every newcomer to play with TON.  
👍 — Web-oriented. Perfect to interact with TON transactions, smart contracts from Web.

👎 — Simplified. It's not possible to receive information where you need an indexed TON API.  
👎 — HTTP-Middleware. You can't fully trust server responses, because they do not contain _Merkle proofs_ to validate that your data is genuine.  

## Get API key

To work with public TonCenter API you need a key:

* Get API key for mainnet: [@tonapibot](https://t.me/tonapibot)
* Get API key for testnet: [@tontestnetapibot](https://t.me/tontestnetapibot)

## RPC Nodes

* [https://toncenter.com/api/v2/](https://toncenter.com/api/v2/) — community-hosted project for Quick Start with API.
* [GetBlock Nodes](https://getblock.io/nodes/ton/) — connect and test your dApps using GetBlocks Nodes.
* [toncenter/ton-http-api](https://github.com/toncenter/ton-http-api) — run your own RPC node.

## SDK

### JavaScript SDK

* [ton-community/ton-js](https://github.com/ton-community/ton) — _Modern_ cross-platform client for TON by the TON Community
* [toncenter/tonweb](https://github.com/toncenter/tonweb) — Cross-platform client for TON by TON Center
* [@tegro/ton3-client](https://github.com/TegroTON/ton3-client) — JS ton3-client by TonHold
* [nns2009/ton-payment-tracker](https://github.com/nns2009/ton-payment-tracker) — TON payment tracker based on TON Center API

### Python SDK

- [tonfactory/tonsdk](https://github.com/tonfactory/tonsdk) — Analogue of the tonweb js library (TON Center HTTP API)

### Elixir SDK

- [ayrat555/ton](https://github.com/ayrat555/ton) - TON SDK for Elixir

## Usage examples

### JavaScript

- [A standard web wallet](https://github.com/toncenter/ton-wallet) (Plain JS)
- [Bridge frontend](https://github.com/ton-blockchain/bridge) (Vue.js)
- [Bot for sales of dumplings](/develop/dapps/tutorials/accept-payments-in-a-telegram-bot-js)

### Python

- [Transfer NFT & Jettons by creating a transfer message from the owner wallet](https://github.com/tonfactory/tonsdk#transfer-nft--jettons-by-creating-a-transfer-message-from-an-owner-wallet)
- [Create mnemonic, init wallet class, create an external message to deploy the wallet](https://github.com/tonfactory/tonsdk#create-mnemonic-init-wallet-class-create-external-message-to-deploy-the-wallet)
- [Storefront bot with payments in TON](/develop/dapps/tutorials/accept-payments-in-a-telegram-bot)
- [Bot with own balance](/develop/dapps/tutorials/accept-payments-in-a-telegram-bot-2)
