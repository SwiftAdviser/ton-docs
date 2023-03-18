---
description: At the end of this guide you will deploy multisig wallet and send some transactions using ton library
---

# Interact with multisig wallets using ton library

## Introduction
If you don't know what is multisig wallet in TON, you can check it out [here](/develop/smart-contracts/tutorials/multisig)

Following this steps you will learn how to:
 * Create and deploy multisig wallet
 * Create, sign and send transactions with that wallet

We will create a TypeScript project and use [ton](https://www.npmjs.com/package/ton) library, so you need to install it first. We will also use the [ton-access](https://www.orbs.com/ton-access/):

```bash
yarn add typescript @types/node ton ton-crypto ton-core buffer @orbs-network/ton-access
yarn tsc --init -t es2022
```

The full code of this guide is available here:
 * https://github.com/Gusarich/multisig-ts-example

## Create and deploy multisig wallet
Let's create a source file, `main.ts` for example. Open it in your favorite code editor and follow this guide!

At first we need to import all important stuff
```js
import { Address, beginCell, MessageRelaxed, toNano, TonClient, WalletContractV4, MultisigWallet, MultisigOrder, MultisigOrderBuilder } from "ton";
import { KeyPair, mnemonicToPrivateKey } from 'ton-crypto';
import { getHttpEndpoint } from "@orbs-network/ton-access";
```

Create `TonClient` instance:
```js
const endpoint = await getHttpEndpoint();
const client = new TonClient({ endpoint });
```
Than we need keypairs to work with:
```js
let keyPairs: KeyPair[] = [];

let mnemonics[] = [
    ['orbit', 'feature', ...], //this should be the seed phrase of 24 words
    ['sing', 'pattern',  ...],
    ['piece', 'deputy', ...],
    ['toss', 'shadow',  ...],
    ['guard', 'nurse',   ...]
];

for (let i = 0; i < mnemonics.length; i++) keyPairs[i] = await mnemonicToPrivateKey(mnemonics[i]);
```
There are two ways to create `MultisigWallet` object:
 * Import existing one from address
  ```js
  let addr: Address = Address.parse('EQADBXugwmn4YvWsQizHdWGgfCTN_s3qFP0Ae0pzkU-jwzoE');
  let mw: MultisigWallet = await MultisigWallet.fromAddress(addr, { client });
  ```

 * Create a new one
  ```js
  let mw: MultisigWallet = new MultisigWallet([keyPairs[0].publicKey, keyPairs[1].publicKey], 0, 0, 1, { client });
  ```

There are also two ways to deploy it
 * Via internal message
  ```js
  let wallet: WalletContractV4 = WalletContractV4.create({ workchain: 0, publicKey: keyPairs[4].publicKey });
  //wallet should be active and have some balance
  await mw.deployInternal(wallet.sender(client.provider(wallet.address, null), keyPairs[4].secretKey), toNano('0.05'));
  ```
 * Via external message
  ```js
  await mw.deployExternal();
  ```

## Create, sign and send an order
We need an `MultisigOrderBuilder` object to create a new order.
```js
let order1: MultisigOrderBuilder = new MultisigOrderBuilder(0);
```
Then we can add some messages to it.
```js
let msg: MessageRelaxed = {
    body: beginCell().storeUint(0, 32).storeBuffer(Buffer.from('Hello, world!')).endCell(),
    info: {
        bounce: true,
        bounced: false,
        createdAt: 0,
        createdLt: 0n,
        dest: Address.parse('EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx'),
        forwardFee: 0n,
        ihrDisabled: true,
        ihrFee: 0n,
        type: "internal",
        value: { coins: toNano('0.01') }
    }
};

order1.addMessage(msg, 3);
```
After you finish with adding messages, transform the `MultisigOrderBuilder` to `MultisigOrder` by calling `build()` method.
```js
let order1b: MultisigOrder = order1.build();
order1b.sign(0, keyPairs[0].secretKey);
```
Now let's create another order, add a message to it, sign it with some other set of keys and union the signatures of these orders.
```js
let order2: MultisigOrderBuilder = new MultisigOrderBuilder(0);
order2.addMessage(msg, 3);
let order2b = order2.build();
order2b.sign(1, keyPairs[1].secretKey);

order1b.unionSignatures(order2b); //Now order1b have also have all signatures from order2b
```
And finally, send the signed order:
```js
await mw.sendOrder(order1b, keyPairs[0].secretKey);
```

Now build the project
```bash
yarn tsc
```

And run the compiled file
```bash
node main.js
```

If it does not throw any errors, you made everything right! Now check if your transaction succeed with any explorer or wallet.

## Other methods and properties
You can easily clear messages from `MultisigOrderBuilder` objects:
```js
order2.clearMessages();
```
You also can clear signatures from `MultisigOrder` objects:
```js
order2b.clearSignatures();
```

And of course you can get public properties from `MultisigWallet`, `MultisigOrderBuilder` and `MultisigOrder` objects

 * MultisigWallet:
    - `owners` - `Dictionary<number, Buffer>` of signatures *ownerId => signature*
    - `workchain` - workchain where the wallet is deployed
    - `walletId` - wallet id
    - `k` - number of signatures required to confirm a transaction
    - `address` - wallet address
    - `provider` - `ContractProvider` instance

 * MultisigOrderBuilder
    - `messages` - array of `MessageWithMode` to be added to the order
    - `querryId` - golbal time until which the order is valid

 * MultisigOrder
    - `payload` - `Cell` with order payload
    - `signatures` - `Dictionary<number, Buffer>` of signatures *ownerId => signature*

## References
 * [Low-level multisig guide](/develop/smart-contracts/tutorials/multisig)
 * [ton.js Documentation](https://ton-community.github.io/ton/)
 * [Multisig contract sources](https://github.com/ton-blockchain/multisig-contract)
