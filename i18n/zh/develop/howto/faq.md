# Frequently Asked Questions

This section covers the most popular questions about TON Blockchain.

## Overview

### Could you share a brief overview of TON?

- [Introduction to The Open Network](/learn/introduction)
- [The TON Blockchain is based on PoS consensus](https://blog.ton.org/the-ton-blockchain-is-based-on-pos-consensus)
- [TON Whitepapers](/learn/docs)

### Similarities and differences versus EVM chains?

- [Ethereum to TON](/learn/introduction#ethereum-to-ton)

### Does TON have a test environment?

- [Testnet](/develop/smart-contracts/environment/testnet)

## Block

### What is the RPC method used to retrieve block information?

Blocks produced by Validators. Existing blocks available via Liteservers. Liteservers accessible via Liteclients. On top of Liteclient built 3rd-party tools like wallets, explorers, dapps, etc.

- Liteclient core: [ton-blockchain/tonlib](https://github.com/ton-blockchain/ton/tree/master/tonlib)

3rd-party high-level block explorers:
- [Explorers for Developers](/participate/explorers)
- https://toncenter.com/
- https://ton.app/explorers

### Block time

_2-5s_

:::info
Read more at [ton.org/analysis](https://ton.org/analysis).
:::

### Time-to-finality

_Under 6 sec._

:::info
Read more at [ton.org/analysis](https://ton.org/analysis).
:::

### Average block size

```bash 
max block size param 29
max_block_bytes:2097152
```

:::info
Find more actual params in [Network Configs](/develop/howto/network-configs).
:::

### What is the schema of a block?

- [Block layout](https://ton.org/docs/tblkch.pdf#page=96&zoom=100,148,172), TON Blockchain, p.96

## Transactions

### RPC method to get transactions data

- [see answer above](/develop/getting-started#what-is-the-rpc-method-used-to-retrieve-block-information)

### Is it async or synchronous? If async, any documentation on how it works?

TON Blockchain is async:
- sender prepare tx body and broadcast it via liteclient (or higher-level tool)
- liteclient return status of broadcast, not tx result
- sender check desired result

Example for Wallet contract transfer (high-level):
- [How TON wallets work and how to access them using JavaScript](https://blog.ton.org/how-ton-wallets-work-and-how-to-access-them-from-javascript#1b-sending-a-transfer)

Example for Wallet contract transfer (low-level):
- https://github.com/xssnick/tonutils-go/blob/master/example/wallet/main.go

### How do we determine if a transaction is truly successful? Is querying the transaction level status enough?

**Short answer:** check receiver's account state until it changed, see examples:
- Go: [Wallet example](https://github.com/xssnick/tonutils-go/blob/master/example/wallet/main.go)
- Python: [Storefront bot with payments in TON](/develop/dapps/tutorials/accept-payments-in-a-telegram-bot)
- JavaScript: [Bot for sales of dumplings](/develop/dapps/tutorials/accept-payments-in-a-telegram-bot-js)

### What is the schema of a transaction?

Fundamentals:

- https://ton.org/docs/tblkch.pdf#page=75&zoom=100,148,290 p.75

Example from explorers (transfer tx):
- https://tonscan.org/tx/FiR7bn5LuBO0FYjx7Fst9kuwnXs128NVFA9YYniKG-A=
- https://ton.cx/tx/33513508000001:FiR7bn5LuBO0FYjx7Fst9kuwnXs128NVFA9YYniKG+A=:EQBfAN7LfaUYgXZNw5Wc7GBgkEX2yhuJ5ka95J1JJwXXf4a8

### Is batching transactions possible?

Yes, this is possible in two ways:
- utilization of async nature of TON, i.e. sending independed transactions to the network
- using smartcontract which receive a task and then execute it as a batch

Example of using batch-featured contract (high-load wallet):
- https://github.com/tonuniverse/highload-wallet-api

## Standards

### What accuracy of currencies is available for TON?

_9 digits_

:::info
Number of decimal places supported by mainnet : 9 digits.
:::

### Is there a standard for tokens and NFTs? i.e. a standard way to parse mint, burn, transfer fungible and non-fungible tokens from a transaction

NFTs:
- [TEP-62: NFT standard](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)
- [Documentation about NFTs](/develop/dapps/defi/tokens#nft)

Jettons (tokens):
- [TEP-74: Jettons standard](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)
- [Distributed TON tokens overview](https://telegra.ph/Scalable-DeFi-in-TON-03-30)
- [Documentation about Jettons](/develop/dapps/defi/tokens#jettons)

Other standards:
- https://github.com/ton-blockchain/TEPs

### Are there examples of parsing these events

Everything in TON is a boc-message, so using NFT isn't a special event, it's a regular message from/to contract as a regular let's say wallet.

However, some indexed API allows you see all messages from/to contract, so you can filter them by your needs:

- https://tonapi.io/swagger-ui


### Please also share how we can get the schema for these events.

https://ton.org/docs/tblkch.pdf#page=53&zoom=100,148,172
p.53

## Account Structure

### What is the address format?

- [Smart Contract Address](/learn/overviews/addresses)

### Is it possible to have a named account similar to ENS

Yes, using TON DNS:
- [What is TON DNS?](/learn/services/dns)

### How to distinguish between a normal account and a smart contract?

- [Everything is a smart contract](/learn/overviews/addresses#everything-is-a-smart-contract)

### How to tell if the address is a token address?

For a **Jettons** contract must implement [standard's interface](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) and return data on _get_wallet_data()_ or _get_jetton_data()_ methods.

### Are there any special accounts (e.g. accounts owned by the network) that have different rules or methods from the rest?

There is a special blockchain inside a TON called masterchain. It consists of network-wide contracts with network configuration, validator-related contracts, etc:

:::info
Read more about masterchain, workchains and shardchains in TON Blockchain overview article: [Blockchain of Blockchains](/learn/overviews/ton-blockchain).
:::

Good example is smart governance contract, which is a part of masterchain:
- [Governance contracts](/develop/smart-contracts/governance)

## Smart Contracts

### How do we detect contract deployment events?

[Everything in TON is a smart contract](/learn/overviews/addresses#everything-is-a-smart-contract).

Account address generated from _private key_, _contract code_, and it's _initial state_.

If any component changed - address changed accordingly. Smart contract code itself can be sent to the network later.

To protect sending messages to non-existing contracts TON use "bounce" feature. Read more in these articles:

- [Deploying wallet via TonLib](https://ton.org/docs/develop/dapps/asset-processing/#deploying-wallet)
- [Paying for processing queries and sending responses](https://ton.org/docs/develop/smart-contracts/guidelines/processing)
- [Tips & Tricks: bounce TON back](https://ton.org/docs/develop/smart-contracts/guidelines/tips)

### Is it possible to re-deploy code to an existing address or do we have to deploy it as a new contract?

Yes, this is possible. If smartcontract implements method ... it's code can be updated and address will remain same.

- https://ton.org/docs/tblkch.pdf#page=30&zoom=100,148,685 p.30

:::info by the way
It's possible to *deploy many contracts with different addresses with **same** private key*.
:::

### Are smart contract addresses case sensitive?

Yes, smart contract addresses are case sensitive because they are generated using the [base64 algorithm](https://en.wikipedia.org/wiki/Base64).  You can learn more about smart contract addresses [here](/docs/learn/overviews/addresses).

## RPC

### Provide a list of recommended node providers for data extraction

API types:
- Read more about different [API Types](/develop/dapps/apis/) (Indexed, HTTP, and ADNL)

Node providers partners:

- [getblock.io](https://getblock.io/)

TON directory with projects from TON Community:

- [ton.app](https://ton.app/)

###  Are there any public node endpoints we can get started with to explore the chain (mainnet and testnet)

- [Network Configs](/develop/howto/network-configs)
- [Examples and tutorials](/develop/dapps/#examples)