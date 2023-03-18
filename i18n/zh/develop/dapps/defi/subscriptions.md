# Subscriptions on TON

Due to the fact that transactions in the TON Blockchain are fast and the network fees are low, you can process recurring payments on-chain via smart contracts.

For example, users can subscribe to digital content (or anything else) and be charged a monthly fee of 1 TON.

There is no specific standard for this.

## Use case flow

The current standard method:

- Users use a v4 wallet. (V4R2 is the TON Blockchain's default wallet smart contract.) It allows additional smart contracts, known as plugins, to extend its functionality.

   After ensuring their functionality, the user can approve the addresses of trusted smart contracts (plugins) for his wallet. Following that, the trusted smart contracts can withdraw Toncoin from the wallet. This is similar to "Infinite Approval" in some other blockchains.

- An intermediate subscription smart contract is used between each user and service as a wallet plugin.

   This smart contract guarantees that a specified amount of Toncoin will be debited from a user's wallet no more than once within a specified period.

- The service's backend initiates payments on a regular basis by sending an external message to subscription smart contracts.

## Smart contract examples

* [Wallet v4 smart contract source code](https://github.com/ton-blockchain/wallet-contract/blob/main/func/wallet-v4-code.fc)
* [Subscription smart contract source code](https://github.com/ton-blockchain/wallet-contract/blob/main/func/simple-subscription-plugin.fc)

## Implementation

A good example of implementation is decentralized subscriptions for Toncoin to private channels in Telegram by the [@donate](https://t.me/donate) bot and the [Tonkeeper wallet](https://tonkeeper.com).