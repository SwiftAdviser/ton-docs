---
description: At the end of the tutorial, you will have deployed multisig contract in TON Blockchain.
---

# How to make a simple multisig contract

## 💡 Overview

This tutorial help you learn how to deploy your multisig contract.  
Recall, that (n, k)-multisig contract is a multisignature wallet with n private keys holders, which accepts requests to send messages if the request (aka order, query) collects at least k signatures of the holders.

Based on original multisig contract code and updates by akifoq:
- [original TON Blockchain multisig-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/multisig-code.fc)
- [akifoq/multisig](https://github.com/akifoq/multisig) with fift libraries to work with multisig.

:::tip starter tip
For anyone new with multisig: [What is Multisig Technology? (video)](https://www.youtube.com/watch?v=yeLqe_gg2u0)
:::

## 📖 What you'll learn

- How to create and customize a simple multisig wallet.
- How to deploy multisig wallet using lite-client.
- How to sign request and send it in message to blockchain.

## ⚙ Set your environment

Before we begin our journey, check and prepare your environment.

- Install `func`, `fift`, `lite-client` binaries and `fiftlib` from the [Installation](/develop/smart-contracts/environment/installation) section.
- Clone [repository](https://github.com/akifoq/multisig) and open its directory in CLI.
```cpp
https://github.com/akifoq/multisig.git
cd ~/multisig
``` 


## 🚀 Let's get started!


1. Compile the code to fift.
2. Prepare multisig owners keys.
3. Deploy your contract.
4. Interact with deployed multisig wallet in blockchain.

### Compile the contract

Compile the contract to Fift with:

```cpp
func -o multisig-code.fif -SPA stdlib.fc multisig-code.fc
```


### Prepare multisig owners keys
#### Create participants keys

To create a key you need to run:

```cpp
fift -s new-key.fif $KEY_NAME$
```

* Where `KEY_NAME` is the name of the file where the private key will be written.

For example:

```cpp
fift -s new-key.fif multisig_key
```

We'll receive a file `multisig_key.pk` with private key inside.

#### Collect public keys

Also, the script will issue a public key in the format:

```
Public key = Pub5XqPLwPgP8rtryoUDg2sadfuGjkT4DLRaVeIr08lb8CB5HW
```

Anything after `"Public key = "` needs to be saved somewhere!

Let's store in file `keys.txt`. One Public Key per line, it's important.

### Deploy your contract

#### Deploy via lite-client

After creating all the keys, you need to collect the public keys into a text file `keys.txt`.

For example:

```bash
PubExXl3MdwPVuffxRXkhKN1avcGYrm6QgJfsqdf4dUc0an7/IA
PubH821csswh8R1uO9rLYyP1laCpYWxhNkx+epOkqwdWXgzY4
```

After that, you need to run:

```cpp
fift -s new-multisig.fif 0 $WALLET_ID$ wallet $KEYS_COUNT$ ./keys.txt
```

* `$WALLET_ID$` - the wallet number assigned for current key. It is recommended to use a unique `$WALLET_ID$` for each new wallet with the same key.
* `$KEYS_COUNT$` - the number of keys needed for confirmation, usually equal to the number of public keys

:::info wallet_id explained
It's possible to create many wallets with the same keys (Alice key, Bob key). What to do if Alice and Bob already have treasure? That's why `$WALLET_ID$` is crucial here.
:::

The script will output something like:

```bash
new wallet address = 0:4bbb2660097db5c72dd5e9086115010f0f8c8501e0b8fef1fe318d9de5d0e501

(Saving address to file wallet.addr)

Non-bounceable address (for init): 0QBLuyZgCX21xy3V6QhhFQEPD4yFAeC4_vH-MY2d5dDlAbel

Bounceable address (for later access): kQBLuyZgCX21xy3V6QhhFQEPD4yFAeC4_vH-MY2d5dDlAepg

(Saved wallet creating query to file wallet-create.boc)
```

:::info 
If you have "public key must be 48 characters long" error, please make sure your `keys.txt` has unix type word wrap - LF. For example, word wrap can be changed via Sublime text editor.
:::

:::tip
Bounceable address is better to keep - this is the address of the wallet.
:::

#### Activate your contract

You need to send some TON to our newly generated _treasure_. For example 0.5 TON.

After that, you need to run lite-client:

```bash
lite-client -C global.config.json
```

:::info Where get `global.config.json`?
You can get fresh config file `global.config.json` for [mainnet](https://ton.org/global-config.json) or [testnet](https://ton.org/testnet-global.config.json).
:::

After starting lite-client, it's best to run the `time` command in lite-client console to make sure the connection was successful:

```bash
time
```

Okay, lite-client is works!

After you need to deploy the wallet. run the command:

```
sendfile ./wallet-create.boc
```

After that, the wallet will be ready to work within a minute.


### Interact with multisig wallet

#### Create a request

First you need to create a message request:

```cpp
fift -s create-msg.fif $ADDRESS$ $AMOUNT$ $MESSAGE$
```

* `$ADDRESS$` - address where to send coins
* `$AMOUNT$` - number of coins
* `$MESSAGE$` - name of file for compiled message.

For example:

```cpp
fift -s create-msg.fif EQApAj3rEnJJSxEjEHVKrH3QZgto_MQMOmk8l72azaXlY1zB 0.1 message
```

:::tip
To add comment for your transaction, use `-C comment` attribute. To get more information, run _create-msg.fif_ file without parameters.
:::

#### Choose a wallet

Next you need to choose a wallet to send a coins from:

```
fift -s create-order.fif $WALLET_ID$ $MESSAGE$ -t $AWAIT_TIME$
```
Where
* `$WALLET_ID$` — is an ID of wallet backed by this multisig contract.
* `$AWAIT_TIME$` — Time in seconds that smart contract will await signs from multisig wallet's owners for request.
* `$MESSAGE$` — here is a name of message boc-file created on the previous step.

:::info
If time equals `$AWAIT_TIME$` passed before the request signs, the request becomes expired. As usual, $AWAIT_TIME$ equals a couple of hours (7200 seconds)
:::

For example:
```
fift -s create-order.fif 0 message -t 7200
```


Ready file will be saved in `order.boc`

:::info
`order.boc` needs to be shared with key holders, they have to sign it.
:::

#### Sign your part

To sign, you need to do:

```bash
fift -s add-signature.fif $KEY$ $KEY_INDEX$
```

* `$KEY$` - name of the file containing the private key to sign, without extension.
* `$KEY_INDEX$` - index of the given key in `keys.txt` (zero-based)

For example, for our `multisig_key.pk` file:

```
fift -s add-signature.fif multisig_key 0
```

#### Create a message

After everyone has signed the order, it needs to be turned into a message for the wallet and signed again with the following command:
```
fift -s create-external-message.fif wallet $KEY$ $KEY_INDEX$
```
In this case, will be enough only one sign of wallet's owner. The idea is that you can't attack a contract with invalid signatures.

For example:
```
fift -s create-external-message.fif wallet multisig_key 0
```

#### Send sign to TON Blockchain

After that, you need to start the light client again:

```bash
lite-client -C global.config.json
```

And after finally, we want to send our sign! Just run:

```bash
sendfile wallet-query.boc
```

If everyone else signed the request, it will be completed!

You did it, ha-ha! 🚀🚀🚀

## What's next?

- [Read more about multisig wallets in TON](https://github.com/akifoq/multisig) from akifoq
