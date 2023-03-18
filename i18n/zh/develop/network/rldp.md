# RLDP

RLDP - Reliable Large Datagram Protocol - is a protocol that runs on top of ADNL UDP, which is used to transfer large data blocks and
includes Forward Error Correction (FEC) algorithms as a replacement of acknowledgment packets on the other side. 
This makes it possible to transfer data between network components more efficiently, but with more traffic consumption.

RLDP is used everywhere in TON infrastructure, for example, to download blocks from other nodes and transfer data to them,
to access TON websites and TON Storage.

## Protocol

RLDP uses the following TL structures for communication:
```tlb
fec.raptorQ data_size:int symbol_size:int symbols_count:int = fec.Type;
fec.roundRobin data_size:int symbol_size:int symbols_count:int = fec.Type;
fec.online data_size:int symbol_size:int symbols_count:int = fec.Type;

rldp.messagePart transfer_id:int256 fec_type:fec.Type part:int total_size:long seqno:int data:bytes = rldp.MessagePart;
rldp.confirm transfer_id:int256 part:int seqno:int = rldp.MessagePart;
rldp.complete transfer_id:int256 part:int = rldp.MessagePart;

rldp.message id:int256 data:bytes = rldp.Message;
rldp.query query_id:int256 max_answer_size:long timeout:int data:bytes = rldp.Message;
rldp.answer query_id:int256 data:bytes = rldp.Message;
```
The serialized structure is wrapped in the `adnl.message.custom` TL schema and sent over ADNL UDP. 
RLDP Transfers are used to transfer big data, a random `transfer_id` is generated, and the data itself is processed by the FEC algorithm. 
The resulting pieces are wrapped in a `rldp.messagePart` structure and sent to the peer until the peer sends us `rldp.complete` or until timeout. 

When the receiver has collected the pieces of `rldp.messagePart` necessary to assemble a complete message, it concat them all together, decodes using FEC and 
deserializes the resulting byte array into one of the `rldp.query` or `rldp.answer` structures, depending on the type (tl prefix id).

### FEC

Valid Forward Error Correction algorithms for use with RLDP are RoundRobin, Online, and RaptorQ.
Currently for data encoding [RaptorQ](https://www.qualcomm.com/media/documents/files/raptorq-technical-overview.pdf) is used.

#### RaptorQ
The essence of RaptorQ is that the data is divided into so-called symbols - blocks of the same, predetermined size.

Matrices are created from blocks, and discrete mathematical operations are applied to them. This allows us to create an almost infinite number of symbols.
from the same data. All symbols are mixed, and it is possible to recover lost packets without requesting additional data from the server, while using fewer packets than it would be if we sent the same pieces in a loop.

The generated symbols are sent to the peer until he reports that all data has been received and restored (decoded) by applying the same discrete operations.

[[Implementation example of RaptorQ in Golang]](https://github.com/xssnick/tonutils-go/tree/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/rldp/raptorq)

## RLDP-HTTP

To interact with TON Sites, HTTP wrapped in RLDP is used. The hoster runs his site on any HTTP webserver and starts rldp-http-proxy next to it. 
All requests from the TON network come via the RLDP protocol to the proxy, and the proxy reassembles the request into simple HTTP and calls the original web server locally.

The user on his side launches the proxy, for example, [Tonutils Proxy](https://github.com/xssnick/TonUtils-Proxy), and uses the `.ton` sites, all traffic is wrapped in the reverse order, requests go to the local HTTP proxy, and it sends them via RLDP to the remote TON site.

HTTP inside RLDP is implemented using TL structures:
```tlb
http.header name:string value:string = http.Header;
http.payloadPart data:bytes trailer:(vector http.header) last:Bool = http.PayloadPart;
http.response http_version:string status_code:int reason:string headers:(vector http.header) no_payload:Bool = http.Response;

http.request id:int256 method:string url:string http_version:string headers:(vector http.header) = http.Response;
http.getNextPayloadPart id:int256 seqno:int max_chunk_size:int = http.PayloadPart;
```
This is not pure HTTP in text form, everything is wrapped in binary TL and unwrapped back to be sent to the web server or browser by the proxy itself.

The scheme of work is as follows:
* Client sends `http.request`
* The server checks the `Content-Length` header when receiving a request
* * If not 0, sends a `http.getNextPayloadPart` request to the client
* * When receiving a request, the client sends `http.payloadPart` - the requested body piece depending on `seqno` and `max_chunk_size`.
* * The server repeats requests, incrementing `seqno`, until it receives all the chunks from the client, i.e. until the `last:Bool` field of the last chunk received is true.
* After processing the request, the server sends `http.response`, the client checks the `Content-Length` header
* * If it is not 0, then sends a `http.getNextPayloadPart` request to the server, and the operations are repeated, as in the case of the client but vice-versa.

## Request the TON Site

To understand how RLDP works, let's look at an example of getting data from the TON site `foundation.ton`. 
Let's say we have already got its ADNL address by calling the Get method of the NFT-DNS contract, [determined the address and port of the RLDP service using DHT](https://github.com/xssnick/ton-deep-doc/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/DHT.md), and [connected to it over ADNL UDP](https://github.com/xssnick/ton-deep-doc/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/ADNL-UDP-Internal.md).

### Send a GET request to `foundation.ton`
To do this, fill in the structure:
```tlb
http.request id:int256 method:string url:string http_version:string headers:(vector http.header) = http.Response;
```

Serialize `http.request` by filling in the fields:
```
e191b161                                                           -- TL ID http.request      
116505dac8a9a3cdb464f9b5dd9af78594f23f1c295099a9b50c8245de471194   -- id           = {random}
03 474554                                                          -- method       = string `GET`
16 687474703a2f2f666f756e646174696f6e2e746f6e2f 00                 -- url          = string `http://foundation.ton/`
08 485454502f312e31 000000                                         -- http_version = string `HTTP/1.1`
01000000                                                           -- headers (1)
   04 486f7374 000000                                              -- name         = Host
   0e 666f756e646174696f6e2e746f6e 00                              -- value        = foundation.ton
```

Now let's wrap our serialized `http.request` into `rldp.query` and serialize it too:
```
694d798a                                                              -- TL ID rldp.query
184c01cb1a1e4dc9322e5cabe8aa2d2a0a4dd82011edaf59eb66f3d4d15b1c5c      -- query_id        = {random}
0004040000000000                                                      -- max_answer_size = 257 KB, can be any sufficient size that we accept as headers
258f9063                                                              -- timeout (unix)  = 1670418213
34 e191b161116505dac8a9a3cdb464f9b5dd9af78594f23f1c295099a9b50c8245   -- data (http.request)
   de4711940347455416687474703a2f2f666f756e646174696f6e2e746f6e2f00
   08485454502f312e310000000100000004486f73740000000e666f756e646174
   696f6e2e746f6e00 000000
```

### Encoding and sending packets

Now we need to apply the FEC RaptorQ algorithm to this data.

Let's create an encoder, for this we need to turn the resulting byte array into symbols of a fixed size. In TON, the symbol size is 768 bytes.
To do this, let's split the array into pieces of 768 bytes. In the last piece, if it comes out smaller than 768, it will need to be padded with zero bytes to the required size.

Our array is 156 bytes in size, which means there will be only 1 piece, and we need to pad it with 612 zero bytes to a size of 768.

Also, constants are selected for the encoder, depending on the size of the data and the symbol, you can learn more about this in the documentation of RaptorQ itself, but in order not to get into mathematical jungle, I recommend using a ready-made library that implements such encoding. 
[[Example of creating an encoder]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/rldp/raptorq/encoder.go#L15) and [[Symbol encoding example]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/raptorq/solver.go#L26).

Symbols are encoded and sent in a round-robin style: we initially define `seqno` which is 0, and increment it by 1 for each successive encoded packet. For example, if we have 2 symbols, then we encode and send the first one, increase seqno by 1, then the second and increase seqno by 1, then again the first one and increase seqno, which at this moment is already equal to 2, by another 1. 
And so until we receive a message that the peer has accepted the data.

Now, when we have created the encoder, we are ready to send data, for this we will fill in the TL schema:
```tlb
fec.raptorQ data_size:int symbol_size:int symbols_count:int = fec.Type;

rldp.messagePart transfer_id:int256 fec_type:fec.Type part:int total_size:long seqno:int data:bytes = rldp.MessagePart;
```
* `transfer_id` - random int256, the same for all messageParts within the same data transfer.
*  `fec_type` is `fec.raptorQ`.
*  * `data_size` = 156
*  * `symbol_size` = 768
*  * `symbols_count` = 1
*  `part` in our case always 0, can be used for transfers that hit the size limit.
*  `total_size` = 156. The size of our transfer data.
*  `seqno` - for the first packet will be equal to 0, and for each subsequent packet it will increase by 1, will be used as parameter to decode and encode symbol.
*  `data` - our encoded symbol, 768 bytes in size.

After serializing `rldp.messagePart`, wrap it in `adnl.message.custom` and send it over ADNL UDP.

We send packets in a loop, increasing seqno all the time, until we wait for the `rldp.complete` message from the peer, or we stop on a timeout. After we have sent a number of packets equal to the number of our symbols, we can slow down and send an additional packet, for example, once every 10 milliseconds or fewer. 
The extra packets are used for recovery in case of data loss, since UDP is a fast but unreliable protocol.

[[Implementation example]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L249)

### Processing the response from `foundation.ton`

During the sending, we can already expect a response from the server, in our case we are waiting for `rldp.answer` with `http.response` inside. 
It will come to us in the same way, in the form of an RLDP transfer, as it was sent at the time of the request, but `transfer_id` will be inverted (each byte XOR 0xFF). 
We will get `adnl.message.custom` messages containing `rldp.messagePart`.

First we need to get the FEC information from the first received message of the transfer, specifically the `data_size`, `symbol_size` and `symbols_count` parameters from the `fec.raptorQ` messagePart structure.
We need them to initialize the RaptorQ decoder. [[Example]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L137)

After initialization, we add the received symbols with their `seqno` to our decoder, and once we have accumulated the minimum required number equal to `symbols_count`, we can try to decode the full message. On success, we will send `rldp.complete`. [[Example]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L168)

The result will be a `rldp.answer` message with the same query_id as in the `rldp.query` we sent. The data must contain `http.response`.
```tlb
http.response http_version:string status_code:int reason:string headers:(vector http.header) no_payload:Bool = http.Response;
```
With the main fields, I think everything is clear, the essence is the same as in HTTP. 
An interesting flag here is `no_payload`, if it is true, then there is no body in the response, (`Content-Length` = 0).
The response from the server can be considered received.

If `no_payload` = false, then there is content in the response, and we need to get it. 
To do this, we need to send a request with a TL schema `http.getNextPayloadPart` wrapped in `rldp.query`.
```tlb
http.getNextPayloadPart id:int256 seqno:int max_chunk_size:int = http.PayloadPart;
```
`id` should be the same as we sent in `http.request`, `seqno` - 0, and +1 for each next part. `max_chunk_size` is the maximum chunk size we are ready to accept, typically 128 KB (131072 bytes) is used.

In response, we will receive:
```tlb
http.payloadPart data:bytes trailer:(vector http.header) last:Bool = http.PayloadPart;
```
If `last` = true, then we have reached the end, we can put all the pieces together and get a complete response body, for example, html.

## References

_Here a [link to the original article](https://github.com/xssnick/ton-deep-doc/blob/master/RLDP.md) by [Oleg Baranov](https://github.com/xssnick)._