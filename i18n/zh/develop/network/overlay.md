# Overlay subnetworks

The architecture of TON is built in such a way that a lot of chains can exist simultaneously and independently in it - they can be both private or public.
Nodes have the ability to choose which shards and chains they store and process.
At the same time, the communication protocol remains unchanged due to its universality. Protocols such as DHT, RLDP and Overlays allow this to be achieved.
We are already familiar with the first two, in this section we will learn what Overlay is.

Overlays are responsible for dividing a single network into additional subnetworks. Overlays can be both public, to which anyone can connect, and private, where additional credentials is needed for entry, known only to a certain amount of people.

All chains in TON, including the masterchain, communicate using their own overlay.
To join it, you need to find the nodes that are already in it, and start exchanging data with them.
For the public overlays you can find nodes using DHT.

## Interaction with overlay nodes

We have already analyzed an example with finding overlay nodes in an article about DHT,
in the section [Search for nodes that store the state of the blockchain](/docs/develop/network/dht#search-for-nodes-that-store-the-state-of-the-blockchain). 
In this section, we will focus on interacting with them.

When querying the DHT, we will get the addresses of the overlay nodes, from which we can find out the addresses of other nodes of this overlay using [overlay.getRandomPeers](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L237) query.
Once we connect to a sufficient number of nodes, we can receive all blocks information and other chain events from them, as well as send our transactions to them for processing.

### Find more neighbors

Let's look at an example of getting nodes in an overlay.

To do this, send a request `overlay.getRandomPeers` to any known node of the overlay, serialize the TL schema:
```tlb
overlay.node id:PublicKey overlay:int256 version:int signature:bytes = overlay.Node;
overlay.nodes nodes:(vector overlay.node) = overlay.Nodes;

overlay.getRandomPeers peers:overlay.nodes = overlay.Nodes;
```
`peers` - should contain the peers we know, so we don't get them back, but since we don't know any yet, `peers.nodes` will be an empty array. 

In case if we want to not just get some information, but participate in overlay and get broadcasts, we should also add in `peers` information about our node, from which we're doing request. 
When peers will get info about us - they will start to send us broadcasts using ADNL or RLDP.

Each request inside the overlay must be prefixed with the TL schema:
```tlb
overlay.query overlay:int256 = True;
```
The `overlay` should be the id of the overlay - the id of the `tonNode.ShardPublicOverlayId` schema key - the same one we used to search the DHT.

We need to concat 2 serialized schemas by simply concatenating 2 serialized byte arrays, `overlay.query` will come first, `overlay.getRandomPeers` second.

We wrap the resulting array in the `adnl.message.query` schema and send it via ADNL. In response, we are waiting for `overlay.nodes` - this will be a list of overlay nodes to which we can connect and, if necessary, repeat the same request to new of them until we get enough connections.

### Functional requests

Once the connection is established, we can access the overlay nodes using [requests](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L413) `tonNode.*`.

For requests of this kind, the RLDP protocol is used. And it's important not to forget the `overlay.query` prefix - it must be used for every query in the overlay.

There is nothing unusual about the requests themselves, they are very similar to what we [did in the article about ADNL TCP](/docs/develop/network/adnl-tcp#getmasterchaininfo).

For example, the `downloadBlockFull` request uses the already familiar schema of block id:
```tlb
tonNode.downloadBlockFull block:tonNode.blockIdExt = tonNode.DataFull;
```
By passing it, we will be able to download the full information about the block, in response we will receive:
```tlb
tonNode.dataFull id:tonNode.blockIdExt proof:bytes block:bytes is_link:Bool = tonNode.DataFull;
  or
tonNode.dataFullEmpty = tonNode.DataFull;
```
If present, the `block` field will contain data in TL-B format.

Thus, we can receive information directly from the nodes.

## References

_Here a [link to the original article](https://github.com/xssnick/ton-deep-doc/blob/master/Overlay-Network.md) by [Oleg Baranov](https://github.com/xssnick)._