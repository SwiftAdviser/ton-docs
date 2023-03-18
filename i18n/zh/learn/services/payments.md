# TON Payments

<img src="/docs/img/docs/ton-payments.jpeg" style={{margin: "20px 0"}} alt="TON Payments overview"/>

On TON Blockchain, block time is about 5 seconds. Even with an increase in network load, that time won’t increase. In other words, in those 5 seconds, millions of transactions can be processed.

Moreover, TON Blockchain has exceptionally low network fees for transactions.

This is enough to solve almost all possible tasks.

In a regular bank app, sending money also takes only a few seconds, but you probably don’t notice because a pretty animation plays during this time.

We don’t see the point in reducing block times to, for example, 500 milliseconds like some other blockchains. Although this is technically possible on TON, this won’t be practically advantageous and network nodes will have to process and store a very large amount of data on their drives. Competing in terms of nominal figures and abstract indicators to the detriment of common sense seems unreasonable to us.

However, there are a few tasks which require lightning-fast transaction speeds and zero network fees.

One example is payment for internet data via TON Proxy or TON Storage, where the cost to download a kilobyte could be 0.000000001 TON (these numbers are used as an example only). Downloading a 1GB file would require millions of microtransactions totaling close to 0.01 TON.

To solve this issue, Payment Channels was created.

## Payment Channels

Payment Channel Technology, or Lightning Network as others call it, is made up of the following:

* Two parties decide that they are going to have a large number of transactions with one another.
* They create a special smart contract on the blockchain where they’ll send their initial balances. For example, Alice and Bob create a channel between themselves and Alice deposits 5 TON whilst Bob deposits 1 TON.
* Next, Alice and Bob can organize transactions between themselves as many times as they want off the blockchain, signing every transaction with a cryptographic algorithm.
* Once Alice and Bob finish all their transacitons, they will sign their respective final balances to close the payments channel and send them to a smart contract that will return their Toncoin according to their final balances. After everything is settled, Alice receives 4 TON back, and Bob gets 2 TON.
* All settlements will happen off the blockchain, meaning they’re free and have no speed restrictions.

A network fee must be paid only twice: upon opening and closing the payments channel.

Nevertheless, the smart contract guarantees proper operations. In the event one of the parties starts to cheat or completely disappears, the other channel’s party will be able to independently close the payments channel and collect the deposited funds by showing a mathematical proof.

:::caution HELP NEEDED
We need the help of contributor here! We want to migrate the article from [payment-channels repository](https://github.com/ton-blockchain/payment-channels) to this section. Read more [how to contribute](/contribute).
:::

:::info
The theory of payment channels is well described in [TON Whitepaper](https://ton.org/docs/ton.pdf), Chapter 5.1.
:::


### Tools

To use payments channels, you don’t need deep knowledge of cryptography.  

* [TON Payments SDK, smart contracts, and examples](/develop/dapps/defi/ton-payments)

## Payment Channels Network

As the technology improves, payments channels will have the capacity to join together in a network off-chain where more than two parties will be able to participate in a channel.

Current smart contracts are already designed to support the functionality of uniting into a single off-chain network.

:::info
The theory of payment channel network is described in [TON Whitepaper](https://ton.org/docs/ton.pdf), chapter 5.2.
:::

## Conclusion

TON Blockchain is fast and has cheap transaction fees. If you need lightning-fast speeds and billions of transactions with zero fees, now you have a tool for that.

The technology behind TON Payments can be applied to a lot of different spheres, such as payments for internet data, streaming, games, DeFi and more!
