# Explorers in TON

In this article, we will consider TON explorers, their capabilities and features from the point of view of the developer.

## What is an explorer?

If you are new to blockchain technology, here is some basic information:

An explorer is a website that allows you to view information in a blockchain, such as the account balance, transaction history, blocks, etc.

## Which explorers exist?

Among TON explorers, you can distinguish several categories:

- For everyday use
- With extended information for developers
- Specialized

This division into categories is largely conditional and one explorer can belong to several categories at the same time. So let's not pay too much attention to this.

## General functionality

Let's start with the general functionality that is present in all explorers.

Almost all explorers have the ability to find out information about balances, transaction history and information about the smart contract, if deployed on the address.

Next, we will consider several explorers that can be attributed to each of these categories.

## TON Scan

Good explorer for everyday use. It has a convenient interface, a lot of information and a search function. Any search is performed by the public [address book](https://github.com/catchain/tonscan/blob/master/src/addrbook.json) (TON Foundation, OKX and etc.)

### Features

- **Convenient for everyday use**
- Convenient for developers
- TON DNS support
- Сontract types
- Contract disassembler

| basic address info                                     | transaction                                           |
| ------------------------------------------------------ | ----------------------------------------------------- |
| ![tonscan](/img/explorers-in-ton/eit-tonscan-info.png) | ![tonscan](/img/explorers-in-ton/eit-tonscan-txn.png) |

### Links

- URL: https://tonscan.org/
- Testnet URL: https://testnet.tonscan.org/

## Ton Whales Explorer

This explorer is more oriented towards developers than ordinary users.

### Features

- **Convenient for developers**
- Сontract types
- Contract disassembler

| basic address info                                         | transaction                                               |
| ---------------------------------------------------------- | --------------------------------------------------------- |
| ![tonwhales](/img/explorers-in-ton/eit-tonwhales-info.png) | ![tonwhales](/img/explorers-in-ton/eit-tonwhales-txn.png) |

### Links

- URL: https://tonwhales.com/explorer

## TON API Explorer

This explorer is the newest and has its own unique features.
For example, Trace. This feature allows you to see the entire sequence of transactions between smart contracts, even if subsequent transactions do not contain your address.

Transaction information is not as detailed as, for example, on TON Whales.

### Features

- Convenient for developers
- Convenient for everyday use
- Jetton transaction history
- **Trace**
- TON DNS support

| basic address info                                   | transaction                                         |
| ---------------------------------------------------- | --------------------------------------------------- |
| ![tonapi](/img/explorers-in-ton/eit-tonapi-info.png) | ![tonapi](/img/explorers-in-ton/eit-tonapi-txn.png) |

### Links

- URL: https://tonapi.io/
- Testnet URL: https://testnet.tonapi.io/

## TON NFT EXPLORER

This explorer specializes in NFTs, but it can also be used as a regular explorer.

When viewing the wallet address, you can find out which NFT it stores and, when viewing the NFT, you can find out the metadata, collection address, owner and transaction history.

### Features

- Convenient for developers
- Сontract types
- **Specialized in NFT**

| nft address info                                             | nft data                                                        |
| ------------------------------------------------------------ | --------------------------------------------------------------- |
| ![tonnft](/img/explorers-in-ton/eit-tonnftexplorer-info.png) | ![tonnft](/img/explorers-in-ton/eit-tonnftexplorer-nftdata.png) |

### Links

- URL: https://explorer.tonnft.tools/
- Testnet URL: https://testnet.explorer.tonnft.tools/

## DTON

DTON is another explorer for developers. It provides a lot of information about transactions in a convenient form.

Also, it has a feature that allows you to see the computation phase of the transaction step by step.

### Features

- Convenient for developers
- Extended information about the computation phase
- Сontract types
- Contract disassembler

| basic address info                               | transaction                                     |
| ------------------------------------------------ | ----------------------------------------------- |
| ![dton](/img/explorers-in-ton/eit-dton-info.png) | ![dton](/img/explorers-in-ton/eit-dton-txn.png) |

### Links

- URL: https://dton.io/

## Want to be in this list?

Please, write to one of the [maintainers](/contribute/maintainers).

## References

- [ton.app/explorers](https://ton.app/explorers)
- [Awesome TON repository](https://github.com/ton-community/awesome-ton)
