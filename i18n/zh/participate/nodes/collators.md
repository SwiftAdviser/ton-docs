# Validator/Collator separation

:::caution in development
This feature is testnet only right now! Participate on your own risk.
:::

The key feature of TON blockchain is the ability to distribute transaction processing over network nodes, and switching from "everybody checks all transactions" to "every transaction is checked by secure validator subset". This ability to infinitely horizontally scale throughput over shards when one workchain splits to required number of *shardchains* distinguishes TON from other L1 networks.

However it is necessary to reguralry rotate validator subsets which process one or another shard to prevent collusion. At the same time to process transactions validators obiviously should know state of the shard prior transaction. The simplest approach is to require all validators to know state of all shards.

This approach works well while number of TON users is within range of a few millions and TPS (transactions per second) is under hundred. However, in the future, when TON will process many thousands transactions per second and server hundred millions or billions of people, no single server would be able to keep actual state of whole network. Fortunately, TON was designed with such loads in mind and supports sharding both throughput and state update.

This is achieived through separation of two roles:
* *Collator* - actor which watch for only part of the network, know actual state and *collate* (generate) next blocks
* *Validator* - actor which gets new blocks from *Collator*, checks it's validity and signs it effectively guaranteeing correctness at the risk of losing the stake.

At the same time architecture of TON allows *Validator* effectively validate new blocks without actually storing state of blockchain, by cheking specially crafted proofs.

That way, when throughput of TON will be to heavy to be processed by single machine, network will consist of subnetwork of collators each of which will process only part of the chains it is capable to process and subnetwork of validators which will form many secure sets for commiting new transactions.

Currently, TON testnet is used for testing this *Validator*/*Collator* separation, where some validators works as usual, and some validators do not collate blocks for themselves and receive them from collators.

# Join with "lite validator"

New node software is available in [block-generation](https://github.com/SpyCheese/ton/tree/block-generation) branch.

## Collator
To create new collator you need to setup TON node; you can use flag `-M` to force node not to keep eye on shardchains it doesn't process.

In `validator-engine-console` create new key for collator, set adnl category `0` to this key and add collation entity through command:
```bash
addcollator <adnl-id> <chain-id> <shard-id>
```

For example:

```bash
newkey
addadnl <adnl-id> 0
addcollator <adnl-id> 0 -9223372036854775808
```

Collator which is configured to shard wc:shard_pfx can collate blocks in shard wc:shard_pfx, its ancestors and its descendants; it also will monitor all shese shards because this is required for collation.

Collator can be stopped with command:
```bash
delcollator <adnl-id> 0 -9223372036854775808
```

:::info
Currently there is one collator in the Network and config **-41** is used to announce it's adnl address.
:::

## Validator
To run validator you need to setup TON node, use flag `--lite-validator` to force validator to request new blocks from collators instead of generating them, and set up staking process. Validator in lite mode takes collator nodes from `-41` config.

The easiest way is the following:
- setup MyTonCtrl for testnet
- Stop validator `sudo systemctl stop validator`
- Update service file `sudo nano /etc/systemd/system/validator.service`: add `--lite-validator` flag
- Reload systemctl `sudo systemctl daemon-reload`
- Start validator `sudo systemctl start validator`

## Lite server

Just like collators, liteservers can be configured to only monitor some part of the blockchain. It can be done by running a node with option `-M` and adding shards in `validator-engine-console`:

```bash
addshard 0 -9223372036854775808
```

Masterchain is always monitored by default. Shards can be removed using `delshard 0 -9223372036854775808`.

### Lite client

Global config should contain at least one of two secions: `liteservers` and `liteservers_v2`. First section contains "full" liteservers which have data about all shard states. Second section contains "partial" liteservers which contain data about some part of the blockchain.

"Partial" liteservers are described as following:

```json
"liteservers_v2": [
  {
    "ip": ...,
    "port": ...,
    "id": {
      "@type": "pub.ed25519",
      "key": "..."
    },  
    "shards": [
      {   
        "workchain": 0, 
        "shard": -9223372036854775808
      }   
    ]   
  }
  ...
]
```

Lite-client and Tonlib support this config and can choose a suitable liteserver for each query. Note that each liteserver monitors masterchain by default, and each server in `liteservers_v2` is implicitly configured to accept queries about masterchain. Shard `wc:shard_pfx` in the config means that the server accepts queries about shard `wc:shard_pfx`, its ancestors and its descendsnts (just like configuration of collators).

## Full collated data
By default validators proposing new block in validator set do not attach data that proves "prior to block" state. This data should be obtained by other validators from locally stored state. That way old (from master branch) and new nodes may reach consensus, but new validators should keep eye on all network state.

Upgrade to new protocol when validators will share blocks with collated data attached can be done by
- Upgrading all validators to new node version
- Setting [full_collated_data](https://github.com/spycheese/ton/blob/block-generation/crypto/block/block.tlb#L737) to true

# Next steps

The practical ability to separate *Validator* and *Collator* roles is the main milestone on the road to limitless throughput, but to create truly decentralised and censorship-resistant network it necessary to
- ensure independence and redundancy of *Collators*
- ensure stable and secure way to interaction of Validators and Collators
- ensure suitable financial model for Collators which incentivize durable collation of new blocks

Currently these tasks are out of the scope.
