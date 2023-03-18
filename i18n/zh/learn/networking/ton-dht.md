# TON DHT Service

Implementation:
* https://github.com/ton-blockchain/ton/tree/master/dht
* https://github.com/ton-blockchain/ton/tree/master/dht-server

## Overview

The Kademlia-like Distributed Hash Table (DHT) plays a crucial role in the networking part of the TON project and is used to locate other nodes in the network.

The keys of the TON DHT are simply 256-bit integers. In most cases, they are computed as a SHA256 of a TL-serialized object.

The values assigned to these 256-bit keys are essentially arbitrary byte strings of limited length. The interpretation of
such byte strings is determined by the preimage of the corresponding key; it
is usually known both by the node that looks up the key and by the node
that stores the key.

In the simplest case, the key represents an ADNL Address of some node and the value can be its IP address and port.

The key-value mapping of the TON DHT is kept on the DHT nodes.

## DHT nodes

Each DHT Node has a 256-bit DHT address. Unlike an ADNL Address, a DHT Address should not change too often, otherwise other nodes would be unable to locate the keys they are looking for.

It is expected that the value of key `K` will be stored on `S` Kademlia-nearest nodes to `K`.

Kademlia distance = 256-bit key `XOR` 256-bit DHT node address (it has nothing to do with geographic location).

`S` is a small parameter, for example `S = 7`, which is needed to improve reliability of
the DHT (if we would keep the key only on one node, the nearest one to `K`,
the value of that key would be lost if that single node goes offline).

## Kademlia routing table

Any node participating in a DHT usually maintains a Kademlia routing table.

It consists of 256 buckets, numbered from 0 to 255. The `i`-th
bucket will contain information about some known nodes (a fixed number
of the “best” nodes and maybe some extra candidates) that lie at a Kademlia
distance from `2^i` to `2^(i+1) − 1` from the node’s address `a`.

This information includes their DHT Addresses, IP Addresses and UDP Ports and
some availability information such as the time and the delay of the last ping.

When a Kademlia node learns about any other Kademlia node as a result
of some query, it places it into a suitable bucket of its routing table, first
as a candidate. Then, if some of the “best” nodes in that bucket fail (e.g., do
not respond to ping queries for a long time), they can be replaced by some
of these candidates. In this way the Kademlia routing table stays populated.

## Key-value pairs

Key-value pairs can be added and updated in the TON DHT.

The “update rules” can  differ. In some cases, they simply
permit replacing the old value with the new value, provided that the new value
is signed by the owner/creator (the signature must be kept as part of the value, to
be checked later by any other nodes after they obtain the value of this key).
In other cases, the old value somehow affects the new value. For example, it
can contain a sequence number and the old value is overwritten only if the
new sequence number is larger (to prevent replay attacks).

TON DHT is not only used to store the IP Addresses of ADNL Nodes, but is also used for other purposes - it can store a list of addresses of the nodes which are storing a specific torrent of TON Storage, a list of addresses of nodes included in an overlay subnetwork, ADNL Addresses of TON services or ADNL Addresses of accounts of the TON Blockchain and so on.

:::info
Read more about TON DHT in [DHT](/docs/develop/network/dht) article, or in Chapter 3.2. of the [TON Whitepaper](https://ton.org/docs/ton.pdf).
:::