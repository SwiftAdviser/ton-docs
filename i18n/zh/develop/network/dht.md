# DHT

DHT stands for Distributed Hash Table and is essentially a distributed key-value database,
where each member of the network can store something, for example, information about themselves.

The implementation of DHT in TON is inherently similar to the implementation of [Kademlia](https://codethechange.stanford.edu/guides/guide_kademlia.html), which is used in IPFS.
Any network member can run a DHT node, generate keys and store data.
To do this, he needs to generate a random ID and inform other nodes about himself.

To determine which node to store the data on, an algorithm is used to determine the "distance" between the node and the key.
The algorithm is simple: we take the ID of the node and the ID of the key, we perform the XOR operation. The smaller the value, the closer the node.
The task is to store the key on the nodes as close as possible to the key, so that other network participants can, using
the same algorithm, find a node that can give data on this key.

## Finding a value by key
Let's look at an example with a search for a key, [connect to any DHT node and establish a connection via ADNL UDP](/docs/develop/network/adnl-udp#packet-structure-and-communication).

For example, we want to find the address and public key for connecting to the node that hosts foundation.ton site. 
Let's say we have already obtained the ADNL address of this site by executing the Get method of the DNS contract. 
The ADNL address in hex representation is `516618cf6cbe9004f6883e742c9a2e3ca53ed02e3e36f4cef62a98ee1e449174`. 
Now our goal is to find the ip, port and public key of the node that has this address.

To do this, we need to get the ID of the DHT key, first we will fill the DHT key schema:
```tlb
dht.key id:int256 name:bytes idx:int = dht.Key
```
`name` is the type of key, for ADNL addresses the word `address` is used, and, for example, to search for shardchain nodes - `nodes`. But the key type can be any array of bytes, depending on the value you are looking for.

Filling in this schema, we get:
```
8fde67f6                                                           -- TL ID dht.key
516618cf6cbe9004f6883e742c9a2e3ca53ed02e3e36f4cef62a98ee1e449174   -- our searched ADNL address
07 61646472657373                                                  -- key type, the word "address" as an TL array of bytes
00000000                                                           -- index 0 because there is only 1 key
```
Next - get the key ID, sha256 hash from the bytes serialized above. It will be `b30af0538916421b46df4ce580bf3a29316831e0c3323a7f156df0236c5b2f75`

Now we can start searching. To do this, we need to execute a query that has [schema](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L197):
```tlb
dht.findValue key:int256 k:int = dht.ValueResult
```
`key` is the id of our DHT key, and `k` is the "width" of the search, the smaller it is, the more accurate, but fewer potential nodes to query. The maximum k for nodes in a TON is 10, usually 6 is used.

Let's populate this structure, serialize and send the request using the `adnl.message.query` schema. [You can read more about this in another article](/docs/develop/network/adnl-udp#packet-structure-and-communication).

In response, we can get:
* `dht.valueNotFound` - if the value is not found.
* `dht.valueFound` - if the value is found on this node.

##### dht.valueNotFound
If we get `dht.valueNotFound`, the response will contain a list of nodes that are known to the node we requested and are as close as possible to the key we requested from the list of nodes known to it. In this case, we need to connect and add the received nodes to the list known to us. 
After that, from the list of all nodes known to us, select the closest, accessible and not yet requested, and make the same request to it. And so on until we try all the nodes in the range we have chosen or until we stop receiving new nodes.

Let's analyze the response fields in more detail, the schemas used:
```tlb
adnl.address.udp ip:int port:int = adnl.Address;
adnl.addressList addrs:(vector adnl.Address) version:int reinit_date:int priority:int expire_at:int = adnl.AddressList;

dht.node id:PublicKey addr_list:adnl.addressList version:int signature:bytes = dht.Node;
dht.nodes nodes:(vector dht.node) = dht.Nodes;

dht.valueNotFound nodes:dht.nodes = dht.ValueResult;
```
`dht.nodes -> nodes` -  list of DHT nodes (array).

Each node has an `id` which is its public key, usually [pub.ed25519](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L47), used as a server key to connect to the node via ADNL. Also, each node has a list of addresses `addr_list:adnl.addressList`, version and signature.

We need to check the signature of each node, for this we read the value of `signature` and set the field to zero (we make it an empty bytes array). After - we serialize the TL structure `dht.node` with the empty signature and check the `signature` field that was before emptying. 
We check on the received serialized bytes, using the public key from `id` field. [[Implementation example]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/dht/client.go#L91)

From the list `addrs:(vector adnl.Address)` we take the address and try to establish an ADNL UDP connection, as the server key we use `id`, which is the public key.

To find out the "distance" to this node - we need to take [key id](/docs/develop/network/adnl-tcp#getting-key-id) from the key from the `id` field and check the distance by the XOR operation from the node's key id and the desired key. 
If the distance is small enough, we can make the same request to this node. And so on, until we find a value or there are no more new nodes.

##### dht.valueFound
The response will contain the value itself, the full key information, and optionally a signature (depends on value type).

Let's analyze the response fields in more detail, the schemas used:
```tlb
adnl.address.udp ip:int port:int = adnl.Address;
adnl.addressList addrs:(vector adnl.Address) version:int reinit_date:int priority:int expire_at:int = adnl.AddressList;

dht.key id:int256 name:bytes idx:int = dht.Key;

dht.updateRule.signature = dht.UpdateRule;
dht.updateRule.anybody = dht.UpdateRule;
dht.updateRule.overlayNodes = dht.UpdateRule;

dht.keyDescription key:dht.key id:PublicKey update_rule:dht.UpdateRule signature:bytes = dht.KeyDescription;

dht.value key:dht.keyDescription value:bytes ttl:int signature:bytes = dht.Value; 

dht.valueFound value:dht.Value = dht.ValueResult;
```
First, let's analyze `key:dht.keyDescription`, it is a complete description of the key, the key itself and information about who and how can update the value.

* `key:dht.key` - the key must match the one from which we took the key ID for the search.
* `id:PublicKey` - the public key of the record owner.
* `update_rule:dht.UpdateRule` - record update rule.
* * `dht.updateRule.signature` - only the owner of the private key can update the record, the `signature` of both the key and the value must be valid
* * `dht.updateRule.anybody` - everyone can update the record, `signature` is empty and not checked
* * `dht.updateRule.overlayNodes` - nodes from the same overlay can update the key, used to find nodes of the same overlay and add yourself

###### dht.updateRule.signature
After reading the description of the key, we act depending on the `updateRule`, for the ADNL address lookup case the type is always `dht.updateRule.signature`. 
We check the key signature in the same way as last time, make the signature an empty byte array, serialize and check. After - we repeat the same for the value, i.e. for the entire `dht.value` object (while returning the key signature to its place).

[[Implementation example]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/dht/client.go#L331)

###### dht.updateRule.overlayNodes
Used for keys containing information about other nodes-shards of the workchain in the network, the value always has the TL structure `overlay.nodes`. 
The value field must be empty.

```tlb
overlay.node id:PublicKey overlay:int256 version:int signature:bytes = overlay.Node;
overlay.nodes nodes:(vector overlay.node) = overlay.Nodes;
```
To check for validity, we must check all `nodes` and for each check `signature` against its `id` by serializing the TL structure:
```tlb
overlay.node.toSign id:adnl.id.short overlay:int256 version:int = overlay.node.ToSign;
```
As we can see, id should be replaced with adnl.id.short, which is the key id (hash) of the `id` field from the original structure. After serialization - we check the signature with the data.

As a result, we get a valid list of nodes that are able to give us information about the workchain shard we need.
###### dht.updateRule.anybody
There are no signatures, anyone can update.

#### Using a value

When everything is verified and the `ttl:int` value has not expired, we can start working with the value itself, i.e. `value:bytes`. For an ADNL address, there must be an `adnl.addressList` structure inside. 
It will contain ip addresses and ports of servers corresponding to the requested ADNL address. In our case, there will most likely be 1 RLDP-HTTP address of the `foundation.ton` service. 
We will use the public key `id:PublicKey` from the DHT key information as the server key.

After the connection is established, we can request the pages of the site using the RLDP protocol. The task from the DHT side at this stage is completed.

### Search for nodes that store the state of the blockchain

DHT is also used to find information about the nodes that store the data of workchains and their shards. The process is the same as when searching for any key, the only difference is in the serialization of the key itself and the validation of the response, we will analyze these points in this section.

In order to get data, for example, of the masterchain and its shards, we need to fill in the TL structure:
```
tonNode.shardPublicOverlayId workchain:int shard:long zero_state_file_hash:int256 = tonNode.ShardPublicOverlayId;
```
Where `workchain` in the case of a masterchain will be equal to -1, its shard will be equal to -922337203685477580 (0xFFFFFFFFFFFFFFFF), and `zero_state_file_hash` is the hash of the zero state of the chain (file_hash), like other data, it can be taken from the global network config, in the `"validator"` field
```json
"zero_state": {
  "workchain": -1,
  "shard": -9223372036854775808, 
  "seqno": 0,
  "root_hash": "F6OpKZKqvqeFp6CQmFomXNMfMj2EnaUSOXN+Mh+wVWk=",
  "file_hash": "XplPz01CXAps5qeSWUtxcyBfdAo5zVb1N979KLSKD24="
}
```
After we have filled in `tonNode.shardPublicOverlayId`, we serialize it and get the key id from it by hashing (as always).

We need to use the resulting key ID as `name` to fill in the `pub.overlay name:bytes = PublicKey` structure, wrapping it in TL bytes array. Next, we serialize it, and we get the key ID now from it.

The resulting id will be the key to use in `dht.findValue`, and the `name` field's value will be the word `nodes`. We repeat the process from the previous section, everything is the same as last time, but `updateRule` will be [dht.updateRule.overlayNodes](#dhtupdateruleoverlaynodes).

After validation - we will get the public keys (`id`) of the nodes that have information about our workchain and shard. To get the ADNL addresses of the nodes, we need to make IDs from the keys (using the hashing method) and repeat the procedure described above for each of the ADNL addresses, as with the ADNL address of the `foundation.ton` domain.

As a result, we will get the addresses of the nodes from which, if we want, we can find out the addresses of other nodes of this chain using [overlay.getRandomPeers](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L237). 
We will also be able to receive all the information about the blocks from these nodes.

## References

_Here a [link to the original article](https://github.com/xssnick/ton-deep-doc/blob/master/DHT.md) by [Oleg Baranov](https://github.com/xssnick)._