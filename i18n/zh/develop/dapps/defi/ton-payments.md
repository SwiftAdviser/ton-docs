# TON Payments

TON Payments is the platform for micropayment channels. 

It allows instant payments without the need to commit all transactions to the blockchain, pay the associated transaction fees (e.g., for the gas consumed), and wait five seconds until the block
containing the transactions in question is confirmed.

Because the overall expense of such instant payments is so minimal, they can be used for micropayments in games, APIs, and off-chain apps. [See examples](/develop/dapps/defi/ton-payments#examples).

* [TON Payments overview article](/learn/services/payments)

## Payment channels

### Smart contracts

* [ton-blockchain/payment-channels](https://github.com/ton-blockchain/payment-channels)

### SDK

To use payment channels, you don’t need deep knowledge of cryptography.

You can use prepared SDKs:

* [toncenter/tonweb](https://github.com/toncenter/tonweb)  JavaScript SDK
* [toncenter/payment-channels-example](https://github.com/toncenter/payment-channels-example)—how to use a payments channel with tonweb.

### Examples

Find examples of using payment channels in the [Hack-a-TON #1](https://ton.org/hack-a-ton-1) winners:

* [grejwood/Hack-a-TON](https://github.com/Grejwood/Hack-a-TON)—OnlyTONs payments project ([website](https://main.d3puvu1kvbh8ti.amplifyapp.com/), [video](https://www.youtube.com/watch?v=38JpX1vRNTk))
* [nns2009/Hack-a-TON-1_Tonario](https://github.com/nns2009/Hack-a-TON-1_Tonario)—OnlyGrams payments project ([website](https://onlygrams.io/), [video](https://www.youtube.com/watch?v=gm5-FPWn1XM))
* [sevenzing/hack-a-ton](https://github.com/sevenzing/hack-a-ton)—Pay-per-Request API usage in TON ([video](https://www.youtube.com/watch?v=7lAnbyJdpOA&feature=youtu.be))
* [illright/diamonds](https://github.com/illright/diamonds)—Pay-per-Minute learning platform ([website](https://diamonds-ton.vercel.app/), [video](https://www.youtube.com/watch?v=g9wmdOjAv1s))