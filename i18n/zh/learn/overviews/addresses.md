# Smart Contract Address

After reading this article you will understand how the actors became smart contracts, what the smart-contract address is in TON, and from which parts it consists.

## Everything is a smart contract

We started from [Actor model](/learn/overviews/ton-blockchain#single-actor). In fact, actors in TON are technically represented as smart contracts. This means that even your wallet is a simple actor (and smart contract).

Usually, actor processes incoming messages, changes own internal state and generates some outbound messages as a result. That's why every actor (i.e. smart contract) in TON Blockchain must have an _address_ to be possible to receipt message from other actors.

:::info EVM EXPERIENCE
You probably got used that _Addresses_ are something different from smart contracts in EVM. Dive in to the differences by article ["Six unique aspects of TON Blockchain that will surprise Solidity developers"](https://blog.ton.org/six-unique-aspects-of-ton-blockchain-that-will-surprise-solidity-developers) by Tal Kol.
:::

## Address of Smart Contract

Smart contract address in the TON Network always consists of two parts:

* **(workchain_id)** the workchain ID (a signed 32-bit integer)
* **(account_id)** the address of the account (64-512 bits depending on the workchain).

Later, in raw address overview we will see how **(workchain_id, account_id)** pair looks like.

### Workchain ID, Account ID

#### Workchain ID

[As we've seen before](/learn/overviews/ton-blockchain#workchain-blockchain-with-your-own-rules), there could be up to `2^32` workchains in TON Blockchain. By this 32-bit prefix in smart contract address you understand to which workchain it belongs, so that TON will send a message in it.

Nowadays, only the Masterchain (workchain_id=-1) and occasionally the basic workchain (workchain_id=0) are running in the TON Blockchain.

Both of them have 256-bit addresses, so we henceforth assume that workchain_id is either 0 or -1 and that the address inside the workchain is exactly 256-bit.

#### Account ID

All account IDs have 256-bit address in the MasterChain and BaseChain (basic workchain).

In fact, Account ID **(account_id)** it's a hash function of a smart contract object (for example, SHA256). Every smart contract has always at least 2 things stored in TON Blockchain:

1. _Compiled code_. By this way, your smart contract reacts to inbound messages.
2. _Initial state_. TL-B scheme of the smart contract.

Combined these 2 parts becomes _StateInit_ structure.

Finally, to receive address of the account TON will calculate a hash of the StateInit object. We won't go deep to the [TVM](/learn/tvm-instructions/tvm-overview) right now, but it's important to understand the concept:

**account_id = hash(StateInit)**

You will read more about technical information in TVM, TL-B and other articles later. But now you know the core concept behind the formation of **account_id** of smart contract address.

## Raw and user-friendly addresses

Under the conditions stated above, the smart-contract address can be represented in the following forms: _raw_ and _user-friendly_.

Raw form is easier to understand for new people in TON, while user-friendly one is used widely across all the apps in the ecosystem.  Let's dive in to the differences and discover why user-friendly address was created.

### Raw address

A raw smart contract address consists of **(workchain_id, account_id)** in this format:

* [decimal workchain_id\]:[64 hexadecimal digits with account_id\]


Finally, we get a _raw smart contract address_  in format **(workchain_id, account_id)**:

`-1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260`

Here you could see `-1`, which is a _workchain_id_ of the MasterChain.

:::note
Notice that uppercase Latin letters 'A'..'F' may be used instead of 'a'..'f' too.
:::

#### What's the problem?

But this approach of smart-contract address has 2 serious cons:

1. It's not possible to verify address for mistakes before sending message.  
_For example, if you have added one symbol by mistake you'll lose your money._
2. It's not possible to add any special flags as you can in user-friendly version.  
_We will cover which flags you can use below._

### User-friendly address

User-friendly address was created to secure and simplify experience for the end users of TON who will share address on the web, inside the Telegram and in real life.

#### How to obtain user-friendly address?

"User-friendly" address is obtained by generating:

1. _[1 byte for flag]_ — Flag changes the way smart-contract reacts to the message.  
Flags of the user-friendly address:
   - isBounceable. (_0x11_ for "bounceable", _0x51_ for "non-bounceable")
   - isTestnetOnly. Add _0x80_ if the address should not be accepted by software running in the production network.
   - isUrlSafe. Deprecated flag, as all addresses are url safe now.
2. _\[1 byte for workchain_id]_ — A signed 8-bit integer with the _workchain_id_.  
(_0x00_ for the BaseChain, _0xff_ for the MasterChain)
3. _\[32 bytes account_id]_ — 256 bits address inside the workchain. ([big-endian](https://www.freecodecamp.org/news/what-is-endianness-big-endian-vs-little-endian/))
4. _\[2 bytes for verification]_ — CRC16-CCITT signature of the previous 34 bytes. ([example](https://github.com/andreypfau/ton-kotlin/blob/ce9595ec9e2ad0eb311351c8a270ef1bd2f4363e/ton-kotlin-crypto/common/src/crc32.kt))
In fact, the idea of verification is pretty similar to the [Luhn algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm) used in every bank card in the world to prevent you from writing non-existing card number by mistake.

Finally, you will have `1 + 1 + 32 + 2 = 36` bytes totally!

To get "user-friendly" address, you need to encode the obtained 36 bytes using either:
- _base64_ (i.e., with digits, upper and lowercase Latin letters, '/' and '+')
- _base64url_ (with '_' and '-' instead of '/' and '+')

After that you receive a "user-friendly" address with a length of 48 non-space characters.

:::info FLAG in DNS address
In TON it's possible to use DNS address like `mywallet.ton` instead of raw and user-friendly form. In fact, DNS address covers the user-friendly address with all the flags inside. So you can get all the flags from the DNS record of the TON domain.
:::

#### Example of user-friendly address

For example, the "test giver" (a special smart contract residing in the masterchain of the Testnet that gives up to 20 test coins to anybody who asks) has raw address:

`-1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260`

Let's convert "test giver" raw address to the user-friendly form:

* `kf/8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15+KsQHFLbKSMiYIny` (base64)
* `kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny` (base64url)

:::info
Notice that both forms (_base64_ and _base64url_) are valid and must be accepted!
:::

#### Bounceable vs non-bounceable addresses

The core idea behind the "bounceable" flag is security for sender.

For example, if the destination smart contract does not exist, or if it throws an unhandled exception while processing this message, the message will be "bounced" back carrying the remainder of the original value (minus all message transfer and gas fees).

In fact, **bounceable=false** means that receiver is a wallet and **bounceable=true** is a custom smart contract with own logic (for example, DEX) and you shouldn't send him any non-bounceable messages because of the security reasons.

Read more in [Non-bounceable messages](/develop/smart-contracts/guidelines/non-bouncable-messages) article.

#### Did you know?

Incidentally, other binary data related to the TON Blockchain has similar "armored" base64 representations, differing by their first bytes. For example, the ubiquitous 256-bit Ed25519 public keys are represented by first creating a 36-byte sequence as follows:
- one tag byte _0x3E_, meaning that this is a public key
- one tag byte _0xE6_, meaning that this is a Ed25519 public key
- 32 bytes containing the standard binary representation of the Ed25519 public key
- 2 bytes containing the big-endian representation of CRC16-CCITT of the previous 34 bytes

The resulting 36-byte sequence is converted into a 48-character base64 or base64url string in the standard fashion. For example, the Ed25519 public key `E39ECDA0A7B0C60A7107EC43967829DBE8BC356A49B9DFC6186B3EAC74B5477D` (usually represented by a sequence of 32 bytes `0xE3, 0x9E, ..., 0x7D`) has the following "armored" representation:

`Pubjns2gp7DGCnEH7EOWeCnb6Lw1akm538YYaz6sdLVHfRB2`


### Convert User-friendly/raw address

The most simple way to convert address by hand is a bunch of official tools and APIs:

* [ton.org/address](https://ton.org/address)
* [toncenter API methods in mainnet](https://toncenter.com/api/v2/#/accounts/pack_address_packAddress_get)
* [toncenter API methods in testnet](https://testnet.toncenter.com/api/v2/#/accounts/pack_address_packAddress_get)

Also, there are 2 ways to work with wallets using JavaScript:

* [Convert address from/to user-friendly or raw form using ton.js](https://github.com/ton-community/ton/blob/master/src/address/Address.spec.ts)
* [Convert address from/to user-friendly or raw form using tonweb](https://github.com/toncenter/tonweb/tree/master/src/utils#address-class)

It's possible to find the same methods in [SDK](/develop/dapps/#most-popular-sdk) for other languages too.

