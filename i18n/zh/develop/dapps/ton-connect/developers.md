# TON Connect for Developers

**Before you start implementing TON Connect in your application or service, we recommend to read the following documentation.**

This is the implementation of the TON Connect. To find more details about TON Connect protocol see the dedicated [docs](https://github.com/ton-connect/docs). Also you can observe example of the TON Connect integration in the dapp on [Github](https://github.com/ton-connect/demo-dapp).

Repository contains three packages:

- ​[@tonconnect/sdk](https://www.npmjs.com/package/@tonconnect/sdk)​
- ​[@tonconnect/protocol](https://www.npmjs.com/package/@tonconnect/protocol)​
- @tonconnect/ui

## TON Connect SDK

- ​[GitHub](https://github.com/ton-connect/sdk/tree/main/packages/sdk)​
- ​[NPM](https://www.npmjs.com/package/@tonconnect/sdk)​

Use it to connect your app to TON wallets via TON Connect protocol. You can find the full description in the link above.

## TON Connect protocol models

- ​[GitHub](https://github.com/ton-connect/sdk/tree/main/packages/protocol)​
- ​[NPM](https://www.npmjs.com/package/@tonconnect/protocol)​

This package contains protocol requests, responses and event models and encoding, decoding functions. You can use it to integrate TON Connect to your wallet app (written with TypeScript). If you want to integrate TON Connect to your dapp, you should use [@tonconnect/sdk](https://www.npmjs.com/package/@tonconnect/sdk).

## TON Connect UI

This package is work in progress right now. It will allow you to integrate TON Connect to your app easier using our UI elements such as "connect wallet button", "select wallet dialog" and confirmation modals.

Basic example of an app functionality in the dapp browser: [GitHub](https://ton-connect.github.io/demo-dapp/)​

Example of a backend part of the dapp above [GitHub](https://github.com/ton-connect/demo-dapp-backend)​

Bridge server on Go: [GitHub](https://github.com/ton-connect/bridge)​

​

## Coming soon

In the near future, the standard TON Connect UI will be available to all developers, including:

- modal wallet selection window;

- connect button;

- interfaces for connecting and signing transactions, etc.

This kit will simplify the implementation of TON Connect in your apps. Standard frontend frameworks will be supported, as well as applications implemented without frameworks

For additional issues in the process of TON Connect 2.0 implementation, you should to contact with our team in the special chat: [Telegram chat for the Developers](https://t.me/tonkeeperdev)​

​

If you have any issues or proposals, you can send it directly through appropriate [GitHub directory](https://github.com/ton-connect/).
