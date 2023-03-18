# Types of Wallet Contracts

You have probably heard somewhere about different versions of wallets in TON Blockchain. But what do these versions really mean and how do they differ?

In this article, we'll look at all versions and modifications of TON wallets.

## How can wallets be different?

Before we start, we need to understand how wallets can differ at all.

If we look at Ethereum, Solana or almost any other blockchain, there are not different types or versions of wallets. But why do they exist in TON? It's because wallets in TON are made by smart contracts. Basically, any wallet (even yours) is a smart contract running on TON Blockchain which can accept and send transactions to other wallets which are also smart contracts.

These smart contracts can be set up in different ways and can have different features. That's why there are several versions of wallets in TON.

## Basic wallets

### Wallet V1

This is the simplest one. It only allows you to send one transaction at the time and it doesn't check anything besides your signature and seqno.

This version isn't even used in regular apps because it has some major issues:
 - No easy way to retrieve the seqno and public key from the contract
 - No `valid_until` check, so you can't be sure that the transaction won't be confirmed too late.

The first issue is fixed in `V1R2` and `V1R3`. That `R` letter means `revision`. Usually revisions are just small updates which only add get-methods which allows you to retrieve seqno and public key from the contract.
But this version also has a second issue, which is fixed in the next version.

Wallet source code:
 * [ton/crypto/smartcont/wallet-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-code.fc) 

### Wallet V2

This version introduces the `valid_until` parameter which is used to set a time limit for a transaction in case you don't want it to be confirmed too late. This version also doesn't have the get-method for public key, which is added in `V2R2`.

It can be used in most cases, but it misses one cool feature, which was added in `V3`.

Wallet source code:
 * [ton/crypto/smartcont/new-wallet-v2.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-wallet-v2.fif)

### Wallet V3

This version introduces the `subwallet_id` parameter, which allows you to create multiple wallets using the same public key (so you can have only one seed phrase and lots of wallets). And, as before, `V3R2` only adds the get-method for public key.

Basically, `subwallet_id` is just a number which is added to the contract state when it is deployed. And since the contract address in TON is a hash of its state and code, the wallet address will change with a different `subwallet_id`.

This version is the most used right now. It covers most use-cases and remains clean and simple.

Wallet source code:
 * [ton/crypto/smartcont/wallet-v3-code.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-v3-code.fif)

### Wallet V4

It is the most modern wallet version at the moment. It still has all the functionality of the previous versions, but also introduces something very powerful — `plugins`.

This feature allows developers to implement complex logic that will work in tandem with a user's wallet. For example, some dApp may require a user to pay a small amount of coins every day to use some features, so the user will need to install the plugin on their wallet by signing a transaction. This plugin will send coins to the destination address every day when it will be reqested by an external message.

This is a very customizable feature which is unique to TON Blockchain.

Wallet source code:
 * [ton-blockchain/wallet-contract](https://github.com/ton-blockchain/wallet-contract)

## Special wallets

Sometimes the functionality of basic wallets isn't enough. That's why there are several types of specialized wallet: `high-load`, `lockup` and `restricted`.

Let's have a look at them.

### High-load wallet

This wallet is made for those who need to send hundreds of transactions in a short period of time. For example, crypto exchanges.

It allows you to send up to `254` transactions in one smart contract call. It also uses a slightly different approach to solve replay attacks instead of seqno, so you can call this wallet several times at once to send even thousands of transactions in a second.

Wallet source code:
 * [ton/crypto/smartcont/highload-wallet-v2-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)

### Lockup wallet

If you, for some reason, need to lock coins in a wallet for some time without the possibility to withdraw them before that time passes, have a look at the lockup wallet.

It allows you to set the time until which you won't be able to withdraw anything from the wallet. You can also customize it by setting unlock periods so that you will be able to spend some coins during these set periods.

For example: you can create a wallet which will hold 1 million coins with total vesting time of 10 years. Set the cliff duration to one year, so the funds will be locked for the first year after the wallet is created. Then, you can set the unlock period to one month, so `1'000'000 TON / 120 months = ~8333 TON` will unlock every month.

Wallet source code:
 * [ton-blockchain/lockup-wallet-contract](https://github.com/ton-blockchain/lockup-wallet-contract)

### Restricted wallet

This wallet's function is to act like a regular wallet, but restrict transfers to only one pre-defined destination address. You can set the destination when you create this wallet and then you'll be only able to transfer funds from it to that address. But note that you can still transfer funds to validation contracts so you can run a validator with this wallet.

Wallet source code:
 * [EmelyanenkoK/nomination-contract/restricted-wallet](https://github.com/EmelyanenkoK/nomination-contract/tree/master/restricted-wallet)

## Conclusion

As you see, there are many different versions of wallets in TON. But in most cases, you only need `V3R2` or `V4R2`. You can also use one of the special wallets if you want to have some additional functionality like a periodic unlocking of funds.

## References

 - [Sources of basic wallets](https://github.com/ton-blockchain/ton/tree/master/crypto/smartcont)
 - [More technical description of versions](https://github.com/toncenter/tonweb/blob/master/src/contract/wallet/WalletSources.md)
 - [Wallet V4 sources and detailed description](https://github.com/ton-blockchain/wallet-contract)
 - [Lockup wallet sources and detailed description](https://github.com/ton-blockchain/lockup-wallet-contract)
 - [Restricted wallet sources](https://github.com/EmelyanenkoK/nomination-contract/tree/master/restricted-wallet)
