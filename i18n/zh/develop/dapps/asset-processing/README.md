# Asset processing on TON
This page contains an overview and specific details that explain how to process (send and accept) digital assets on the TON network.


## Global overview
Embodying a fully asynchronous approach, the TON Blockchain involves a few concepts which are uncommon to traditional blockchains. Particularly, each interaction of any actor with the blockchain consists of a graph of asynchronously transferred messages between smart contracts and/or the external world. The common path of any interaction starts with an external message sent to a `wallet` smart contract, which authenticates the message sender using public-key cryptography, takes charge of fee payment, and sends inner blockchain messages. That way, transactions on the TON network are not synonymous with user interaction with the blockchain but merely nodes of the message graph: the result of accepting and processing a message by a smart contract, which may or may not lead to the emergence of new messages. The interaction may consist of an arbitrary number of messages and transactions and span a prolonged period of time. Technically, transactions with queues of messages are aggregated into blocks processed by validators. The asynchronous nature of the **TON Blockchain does not allow to predict the hash and lt (logical time) of a transaction** at the stage of sending a message. The transaction accepted to the block is final and will not be modified.

**Each inner blockchain message, that is, a message from one smart contract to another, bears some amount of digital assets as well as an arbitrary portion of data.**

Smart contract guidelines recommend treating the data payload, which begins with 32 binary zeros, as a human-readable text message. Most software, such as wallets and libraries, support this specification and allow to send text comments along with Toncoin as well as display comments in other messages.

Smart contracts **pay fees for transactions** (usually from the balance of an incoming message) as well as **a storage fee for the contract's stored code and data**. Fees depend on workchain configs with maximal fees on `masterchain` and substantially lower fees on `basechain`.


## Digital assets on TON
TON has three types of digital assets. The first is Toncoin, the main token of the network. It is used for all basic operations on the blockchain, for example, paying gas fees or staking for validation. The second type is native tokens, which are special kinds of assets that can be attached to any message on the network. These assets are currently not in use since the functionality for issuing new native tokens is closed. Finally, the third type is contract assets, which are analogous to the ERC-20 standard and are managed by arbitrary contracts (there are a few proposed specifications) and thus can require custom rules for processing.

### Simple Toncoin transfer
To send Toncoin, the user needs to send a request via an external message, that is, a message from the outside world to the blockchain, to a special `wallet` smart contract (see below). Upon receiving this request, `wallet` will send an inner message with the desired amount of assets and optional data payload, for instance a text comment.

## Wallet smart contract
Wallet smart contracts are contracts on the TON Network which serve the task of allowing actors outside the blockchain to interact with blockchain entities. Generally, it solves three challenges:
* authenticates owner: Rejects to process and pay fees for non-owners' requests.
* replays protection: Prohibits the repetitive execution of one request, for instance sending assets to some other smart contract.
* initiates arbitrary interaction with other smart contracts.

Standard solution for the first challenge is public-key cryptography: `wallet` stores the public key and checks that an incoming message with a request is signed by the corresponding private key which is known only by the owner. The solution to the third challenge is common as well; generally, a request contains a fully formed inner message `wallet` sends to the network. However, for replay protection, there are a few different approaches.

### Seqno-based wallets
Seqno-based wallets follow the most simple approach to sequencing messages. Each message has a special `seqno` integer that must coincide with the counter stored in the `wallet` smart contract. `wallet` updates its counter on each request, thus ensuring that one request will not be processed twice. There are a few `wallet` versions that differ in publicly available methods: the ability to limit requests by expiration time, and the ability to have multiple wallets with the same public key. However, an inherent requirement of that approach is to send requests one by one, since any gap in `seqno` sequence will result in the inability to process all subsequent requests.

### High-load wallets
This `wallet` type follows an approach based on storing the identifier of the non-expired processed requests in smart-contract storage. In this approach, any request is checked for being a duplicate of an already processed request and, if a replay is detected, dropped. Due to expiration, the contract may not store all requests forever, but it will remove those that cannot be processed due to the expiration limit. Requests to this `wallet` may be sent in parallel without interfering with each other; however, this approach requires more sophisticated monitoring of request processing.

## Interaction with blockchain
Basic operations on the TON Blockchain can be carried out via TonLib. It is a shared library which can be compiled along with a TON node and expose APIs for interaction with the blockchain via so-called lite servers (servers for lite clients). TonLib follows a trustless approach by checking proofs for all incoming data; thus, there is no necessity for a trusted data provider. Methods available to TonLib are listed [in the TL scheme](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234). They can be used either as a shared library via wrappers like [pyTON](https://github.com/EmelyanenkoK/pyTON) or [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2) (technically those are the wrappers for `tonlibjson`) or through `tonlib-cli`.


## Deploying wallet
To deploy a wallet via TonLib one needs to:
1. Generate a private/public key pair via [createNewKey](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L213) or its wrapper functions (example in [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2#create-new-private-key)). Note that the private key is generated locally and does not leave the host machine.
2. Form [InitialAccountWallet](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L60) structure corresponding to one of the enabled `wallets`. Currently `wallet.v3`, `wallet.highload.v1`, `wallet.highload.v2` are available.
3. Calculate the address of a new `wallet` smart contract via the [getAccountAddress](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L249) method. We recommend using a default revision `0` and also deploying wallets in the basechain `workchain=0` for lower processing and storage fees.
4. Send some Toncoin to the calculated address. Note that you need to send them in `non-bounce` mode since this address has no code yet and thus cannot process incoming messages. `non-bounce` flag indicates that even if processing fails, money should not be returned with a bounce message. We do not recommend using the `non-bounce` flag for other transactions, especially when carrying large sums, since the bounce mechanism provides some degree of protection against mistakes.
5. Form the desired [action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L148), for instance `actionNoop` for deploy only. Then use [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255) and [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260) to initiate interactions with the blockchain.
6. Check the contract in a few seconds with [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L254) method.

## Incoming message value
To calculate the incoming value that the message brings to the contract, one needs to parse the transaction. It happens when the message hits the contract. A transaction can be obtained using[getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L236). For an incoming wallet transaction, the correct data consists of one incoming message and zero outgoing messages. Otherwise, either an external message is sent to the wallet, in which case the owner spends Toncoin, or the wallet is not deployed and the incoming transaction bounces back.

Anyway, in general, the amount that a message brings to the contract can be calculated as the value of the incoming message minus the sum of the values of the outgoing messages minus the fee: `value_{in_msg} - SUM(value_{out_msg}) - fee`. Technically, transaction representation contains three different fields with `fee` in name: `fee`, `storage_fee`, and `other_fee`, that is, a total fee, a part of the fee related to storage costs, and a part of the fee related to transaction processing. Only the first one should be used.

## Checking contract's transactions
A contract's transactions can be obtained using [getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L236). This method allows to get 10 transactions from some `transactionId` and earlier. To process all incoming transactions, the following steps should be followed:
1. The latest `last_transaction_id` can be obtained using [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L235)
2. List of 10 transactions should be loaded via the `getTransactions` method.
3. Unseen transactions from this list should be processed.
4. Incoming payments are transactions in which the incoming message has a source address; outgoing payments are transactions in which the incoming message has no source address and also presents the outgoing messages. These transactions should be processed accordingly.
5. If all of those 10 transactions are unseen, the next 10 transactions should be loaded and steps 2,3,4,5 should be repeated.


## Accepting payments
There are a few approaches to accepting payments that differ in their method of distinguishing users.

### Invoice-based approach
To accept payments based on attached comments, the service should
1. Deploy the `wallet` contract.
2. Generate a unique `invoice` for each user. String representation of uuid32 will be enough.
3. Users should be instructed to send Toncoin to the service's `wallet` contract with an attached `invoice` as a comment.
4. Service should regularly poll the getTransactions method for the `wallet` contract.
5. For new transactions, the incoming message should be extracted, `comment` matched against the database, and the value (see **Incoming message value** paragraph) deposited to the user's account.

## Sending payments

1. Service should deploy a `wallet` and keep it funded to prevent contract destruction due to storage fees. Note that storage fees are generally less than 1 Toncoin per year.
2. Service should get from the user `destination_address` and optional `comment`. Note that for the meantime, we recommend either prohibiting unfinished outgoing payments with the same (`destination_address`, `value`, `comment`) set or proper scheduling of those payments; that way, the next payment is initiated only after the previous one is confirmed.
3. Form [msg.dataText](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L98) with `comment` as text.
4. Form [msg.message](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L108) which contains `destination_address`, empty `public_key`, `amount` and `msg.dataText`.
5. Form [Action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L149) which contains a set of outgoing messages.
6. Use [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255) and [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260) queries to send outgoing payments.
7. Service should regularly poll the getTransactions method for the `wallet` contract. Matching confirmed transactions with the outgoing payments by (`destination_address`, `value`, `comment`) allows to mark payments as finished; detect and show the user the corresponding transaction hash and lt (logical time).
8. Requests to `v3` of `high-load` wallets have an expiration time equal to 60 seconds by default. After that time unprocessed requests can be safely resent to the network (see steps 3-6).

## Explorers

The blockchain explorer is https://tonscan.org.

To generate a transaction link in the explorer, the service needs to get the lt (logic time), transaction hash, and account address (account address for which lt and txhash were retrieved via the getTransactions method). https://tonscan.org and https://explorer.toncoin.org/ may then show the page for that tx in the following format:

`https://tonscan.org/tx/{lt as int}:{txhash as base64url}:{account address}`

`https://explorer.toncoin.org/transaction?account={account address}&lt={lt as int}&hash={txhash as base64url}`
