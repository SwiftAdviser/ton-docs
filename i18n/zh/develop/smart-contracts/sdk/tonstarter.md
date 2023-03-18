# Using TypeScript

## Blueprint

Testing toolkit (usually, sandbox) already included to TypeScript SDK named Blueprint.

- [Read more about Blueprint](develop/smart-contracts/sdk/javascript)

Run tests in one line using:

```bash npm2yarn
npm test
```

## Low-level libraries

### sandbox

This package allows you to emulate arbitrary TON smart contracts, send messages to them and run get methods on them as if they were deployed on a real network.

The key difference of this package from ton-contract-executor is the fact that the latter only emulates the compute phase of the contract - it does not know about any other phases and thus does not know anything about fees and balances (in a sense that it does not know whether a contract's balance will be enough to process all the out messages that it produces).

On the other hand, this package emulates all the phases of a contract, and as a result, the emulation is much closer to what would happen in a real network.

- https://github.com/ton-community/sandbox

### ton-contract-executor

:::info deprecated
This library is deprecated. TON Community not developing it anymore.
:::

This library allows you to run TON Virtual Machine locally and execute contract. That allows you to write & debug & fully test your contracts before launching them to the network.

- https://github.com/ton-community/ton-contract-executor

## Tutorials

Read this article first to understand all approaches to testing on TON:

* [TON Hello World part 4: Step by step guide for testing your first smart contract](https://ton-community.github.io/tutorials/04-testing/)