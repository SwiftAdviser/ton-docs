# Blockchain of Blockchains


:::tip
Terms '**smart contract**', '**account**' and '**actor**' are used interchangeably in this document to describe a blockchain entity.
:::

## Single actor

Let's consider one smart contract.

In TON, it is a _thing_ with properties like `address`, `code`, `data`, `balance` and others. In other words, it is an object which has some _storage_ and _behavior_.
That behavior has the following pattern:
* something happens (the most common situation is that a contract gets a message)
* contract handles that event according to its own properties by executing its `code` in TON Virtual Machine.
* contract modifies its own properties (`code`, `data` and others)
* contract optionally generates outgoing messages
* contract goes into standby mode until the next event occurs

A combination of these steps is called a **transaction**. It is important that events are handled one by one, thus _transactions_ are strictly ordered and cannot interrupt each other.

This behavior pattern is well known and called 'Actor'.

### The lowest level: Account Chain

A sequence of _transactions_ `Tx1 -> Tx2 -> Tx3 -> ....` may be called a **chain**. And in the considered case it is called **AccountChain** to emphasize that it is _the chain_ of a single account of transactions.

Now, since nodes that process transactions need from time to time to coordinate the state of the smart contract (to reach a _consensus_ about the state) those _transactions_ are batched:
`[Tx1 -> Tx2] -> [Tx3 -> Tx4 -> Tx5] -> [] -> [Tx6]`.
Batching does not intervene in sequencing, each transaction still has only one 'prev tx' and at most one 'next tx', but now this sequence is cut into the **blocks**. 

It is also expedient to include queues of incoming and outgoing messages to _blocks_. In that case, a _block_ will contain a full set of information which determines and describes what happened to the smart contract during that block.

## Many AccountChains: Shards

Now let's consider many accounts. We can get a few _AccountChains_ and store them together, such a set of _AccountChains_ is called a **ShardChain**. In the same way, we can cut **ShardChain** into **ShardBlocks**, which are an aggregation of individual _AccountBlocks_.

### Dynamic splitting and merging of ShardChains

Note that since a _ShardChain_ consists of easily distinguished _AccountChains_, we can easily split it. That way if we have 1 _ShardChain_ which describes events that happen with 1 million accounts and there are too many transactions per second to be processed and stored in one node, so we just divide (or **split**) that chain into two smaller _ShardChains_ with each chain accounting for half a million accounts and each chain processed on a separate subset of nodes.

Analogously, if some shards became too unoccupied they can be **merged** into one bigger shard.

There are obviously two limiting cases: when the shard contains only one account (and thus cannot be split further) and when the shard contains all accounts.

Accounts can interact with each other by sending messages. There is a special mechanism of routing which move messages from outgoing queues to corresponding incoming queues and ensures that 1) all messages will be delivered 2) messages will be delivered consecutively (the message sent earlier will reach the destination earlier).

:::info SIDE NOTE
To make splitting and merging deterministic, an aggregation of AccountChains into shards is based on the bit-representation of account addresses. For example, address looks like `(shard prefix, address)`. That way, all accounts in the shardchain will have exactly the same binary prefix (for instance all addresses will start with `0b00101`).
:::


## Blockchain

An aggregation of all shards which contains all accounts behaving by one set of rules is called a **Blockchain**.

In TON there can be many sets of rules and thus many blockchains which operate simultaneously and can interact with each other by sending messages crosschain in the same way that accounts of one chain can interact with each other.

### Workchain: Blockchain with your own rules

If you want to customize rules of the group of Shardchains, you could create a **Workchain**. A good example is to make a workchain that works on the base of EVM to run Solidity smart contracts on it.


Theoretically, everyone in community can create own workchain. In fact, it's pretty complicated task to build it, after that to pay (expensive) price of creating it and receive 2/3 of votes from validators to approve creation of your Workchain.

TON allows creating up to `2^30` workchains, each subdivided to up to `2^60` shards.

Nowadays, there are only 2 workchains in TON: MasterChain and BaseChain.

BaseChain is used for everyday transactions between actors because it's pretty cheap, while MasterChain have a crucial function for TON, so let's cover what does it do!

### Masterchain: Blockchain of Blockchains

There is a necessity for the synchronization of message routing and transaction execution. In other words, nodes in the network need a way to fix some 'point' in a multichain state and reach a consensus about that state. In TON, a special chain called **MasterChain** is used for that purpose. Blocks of _masterchain_ contain additional information (latest block hashes) about all other chains in the system, thus any observer unambiguously determines the state of all multichain systems at a single masterchain block.
