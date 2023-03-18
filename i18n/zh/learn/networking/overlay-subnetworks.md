# Overlay Subnetworks

Implementation:
* https://github.com/ton-blockchain/ton/tree/master/overlay

## Overview

In a multi-blockchain system like TON, even full nodes would usually be interested in obtaining updates (i.e., new blocks) only around
a few shardchains. To this end, a special overlay subnetwork has been built
inside the TON Network, on top of the ADNL Protocol,
for each shardchain.

Also, overlay subnetworks are used for the operation of TON Storage, TON Proxy and so on.

## ADNL vs Overlay networks

In contrast to ADNL, the TON overlay networks usually do not support
sending datagrams to other arbitrary nodes. Instead, some “semi-permanent
links” are established between certain nodes (called “neighbors” with respect to
the overlay network under consideration) and messages are usually forwarded
along these links (i.e. from a node to one of its neighbors).

Each overlay subnetwork has a 256-bit network identifier usually equal
to a SHA256 of the description of the overlay network—a TL-serialized object.

Overlay subnetworks can be public or private.

Overlay subnetworks work according to a special [gossip](https://en.wikipedia.org/wiki/Gossip_protocol) protocol.

:::info
Read more about overlays in [Overlay subnetworks](/docs/develop/network/overlay) article, or in Chapter 3.3 of the [TON Whitepaper](https://ton.org/docs/ton.pdf).
:::

