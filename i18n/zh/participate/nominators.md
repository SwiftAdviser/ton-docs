# Nominator Pools

## Overview 

With TON smart contracts, you can implement any staking and deposit mechanics you want.

However, there is "native staking" in TON Blockchain - you can lend Toncoin to validators for staking and share the reward for validation.

The one who lends to validator is called the **nominator**.

A smart contract, called a **nominator pool**, provides the ability for one or more nominators to lend Toncoin in a validator stake, and ensures that the validator can use that Toncoin only for validation. Also, the smart contract guarantees the distribution of the reward.


## Validators vs Nominators

If you are familiar with cryptocurrencies, you must have heard about **validators** and **nominators**. These words often appear in crypto-related channels (our channel is no exception). Now, the time has come to find out what they are – the two major actors ruling the blockchain.

### Validators

First, let's speak about validators. A validator is a network node that helps keep the blockchain running by verifying (or validating) suggested blocks and recording them on the blockchain.

To become a validator, you must meet two requirements: have a high-performance server and obtain a serious amount of TON (600,000) in order to make a stake. At the time of writing, there are 227 validators on TON.

### Nominators

It's evident that not everyone can afford to have 100,000s of Toncoin on their balance – here's where nominators come into play. Simply put, the nominator is a user who lends his TON to validators. Every time the validator earns a reward by validating blocks, it is distributed between the involved participants.

Some time ago, Ton Whales ran the first staking pool on TON with a minimum deposit of 50 TON. Later, TON Foundation launched the first open nominator pool. Now, users may stake Toncoin in a fully-decentralized way, starting with **10,000 TON**.

_From [TON Community post](https://t.me/toncoin/543)._

## How to participate?

* [The list of the TON nominator pools](https://tonvalidators.org/)

## Source code

* [Nominator Pool smart contract source code](https://github.com/ton-blockchain/nominator-pool)

:::info
The theory of nominators is described in [TON Whitepaper](https://ton.org/docs/ton.pdf), chapters 2.6.3, 2.6.25.
:::