# TON Networking

The TON Project uses its own peer-to-peer network protocols.

- **TON Blockchain uses these protocols** to propagate new blocks, send and collect transaction candidates and so on.

  While the networking demands of single-blockchain projects, such as Bitcoin or Ethereum, can be met quite easily (one essentially needs to construct
  a peer-to-peer overlay network and then propagate all new blocks and
  transaction candidates via a [gossip](https://en.wikipedia.org/wiki/Gossip_protocol) protocol), whereas multi-blockchain projects, such
  as TON, are much more demanding (e.g. one must be able to
  subscribe to updates of only some shardchains, not necessarily all of them).


- **TON Ecosystem services (e.g. TON Proxy, TON Sites, TON Storage) run on these protocols.**

  Once the more sophisticated network protocols needed
  to support TON Blockchain are in place, it turns out that they can easily
  be used for purposes not necessarily related to the immediate demands of the
blockchain itself, thus providing more possibilities and flexibility for creating
  new services in the TON Ecosystem.

