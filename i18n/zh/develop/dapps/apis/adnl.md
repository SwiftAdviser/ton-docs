# TON ADNL API

Clients connect directly to lite servers (nodes) using a binary protocol.

The client downloads keyblocks, the current state of the account, and their **Merkle proofs**, which guarantees the validity of the received data.

Read operations (like get-method calls) are made by launching a local TVM with a downloaded and verified state.

There is no need to download the full state of the blockchain, the client downloads only what is needed for the operation. Calling the local TVM is also ineffective.

You can connect to public lite servers from the global config ([mainnet](https://ton.org/global-config.json) or [testnet](https://ton.org/testnet-global.config.json)) or run your own lite server.

Read more about Merkle proofs at [TON Whitepaper](https://ton.org/ton.pdf) 2.3.10, 2.3.11.

## Pros & Cons

👍 — Reliable. Uses API with Merkle proof hashes to verify incoming binary data.  
👍 — Secure. Since it checks Merkle proofs, you can even use untrusted lite servers.  
👍 — Fast. Instead of HTTP-middleware directly connects to TON Blockchain nodes. 

👎 — Complicated. More time is required to figure things out.  
👎 — Back-end first. Not compatible with web frontends (built for non-HTTP protocol).

## API reference

Requests and responses to the server are described by a TL schema that allows you to generate a typed interface for a certain programming language.

[TonLib TL Schema](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl)

## SDK

### Golang SDK

- [xssnick/tonutils-go](https://github.com/xssnick/tonutils-go) — _Modern_ Golang SDK for the TON Blockchain.
- [startfellows/tongo](https://github.com/startfellows/tongo) — Golang SDK with native ADNL support, cells manipulations and CGO for TVM and tx emulations.

### Kotlin & Java SDK

- [ton-kotlin](https://github.com/andreypfau/ton-kotlin) — Kotlin SDK for the TON Blockchain.

### Python SDK

- [psylopunk/pytonlib](https://github.com/psylopunk/pytonlib) — Newbie-friendly Python SDK (ADNL API)
- [toncenter/pytonlib](https://github.com/toncenter/pytonlib) — Python SDK (ADNL API)

### Legacy TonLib SDK

These SDKs are _long-term support_ stage, so feel free to use these SDK too.

- [C++ TonLib](https://github.com/ton-blockchain/ton/tree/master/example/cpp)
- [Python TonLib wrapper](https://github.com/toncenter/pytonlib)
- [Golang TonLib wrapper](https://github.com/ton-blockchain/tonlib-go)
- [Java TonLib wrapper (JNI)](https://github.com/ton-blockchain/tonlib-java)


## Usage examples

### Python

- [psylopank/pytonlib examples](https://github.com/psylopunk/pytonlib/tree/main/examples)

### Go

- [10+ examples from xssnick/tonutils-go](https://github.com/xssnick/tonutils-go/tree/master/example)

### Legacy TonLib SDK

- [Desktop standard wallet](https://github.com/ton-blockchain/wallet-desktop) (C++ and Qt)
- [Android standard wallet](https://github.com/ton-blockchain/wallet-android) (Java)
- [iOS standard wallet](https://github.com/ton-blockchain/wallet-ios) (Swift)
- [TonLib CLI](https://github.com/ton-blockchain/ton/blob/master/tonlib/tonlib/tonlib-cli.cpp) (C++)
