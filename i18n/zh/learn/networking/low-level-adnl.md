# Low-Level ADNL 

Abstract Datagram Network Layer (ADNL) is the core protocol of TON, which helps network peers to communicate with each other.

## Peer identity
Each peer must have at least one identity, it is possible but not necessary to use multiple. Each identity is a keypair, which is used to perform the Diffie-Hellman between peers. An abstract network address is derived from the public key in such way: `address = SHA-256(type_id || public_key)`. Note that type_id must be serialized as little-endian uint32.

## Public-key cryptosystems list
| type_id    | cryptosystem        |
|------------|---------------------|
| 0x4813b4c6 | ed25519<sup>1</sup> |

_1. To perform x25519, the keypair must be generated in x25519 format. However, the public key is transmitted over the network in ed25519 format, so you have to convert the public key from x25519 to ed25519, examples of such conversions can be found [here](https://github.com/tonstack/adnl-rs/blob/master/src/integrations/dalek.rs#L10) for Rust and [here](https://github.com/andreypfau/curve25519-kotlin/blob/f008dbc2c0ebc3ed6ca5d3251ffb7cf48edc91e2/src/commonMain/kotlin/curve25519/MontgomeryPoint.kt#L39) for Kotlin._

## Client-server protocol (ADNL over TCP)
The client connects to the server using TCP and sends an ADNL handshake packet, which contains a server abstract address, a client public key and encrypted AES-CTR session parameters, which are determined by the client.

### Handshake
First, the client must perform a key agreement protocol (for example, x25519) using their private key and server public key, taking into account the server key's `type_id`. As a result, the client will gain `secret`, which is used to encrypt session keys in future steps.

Then, the client has to generate AES-CTR session parameters, a 16-byte nonce and 32-byte key, both for TX (client->server) and RX (server->client) directions and serialize it into a 160-byte buffer as follows:

| Parameter    | Size     |
|--------------|----------|
| rx_key       | 32 bytes |
| tx_key       | 32 bytes |
| rx_nonce     | 16 bytes |
| tx_nonce     | 16 bytes |
| padding      | 64 bytes |

The purpose of padding is unknown, it is not used by server implementations. It is recommended to fill the whole 160-byte buffer with random bytes, otherwise an attacker may perform an active MitM attack using compromised AES-CTR session parameters.

The next step is to encrypt session parameters using `secret` via the key agreement protocol above. To do that, AES-256 must be initialized in CTR mode with a 128-bit big-endian counter using a (key, nonce) pair which is computed as such (`aes_params` is a 160-byte buffer which was built above):
```cpp
hash = SHA-256(aes_params)
key = secret[0..16] || hash[16..32]
nonce = hash[0..4] || secret[20..32]
```
After the encryption of `aes_params` which is noted as `E(aes_params)`, AES should be removed because it is not needed anymore.

Now we are ready to serialize all that information to the 256-bytes handshake packet and send it to the server:

| Parameter           | Size      | Notes                                                      |
|---------------------|-----------|------------------------------------------------------------|
| receiver_address    | 32 bytes  | Server peer identity as described in the corresponding section |
| sender_public       | 32 bytes  | Client public key                                          |
| SHA-256(aes_params) | 32 bytes  | Integrity proof of session parameters                      |
| E(aes_params)       | 160 bytes | Encrypted session parameters                               |

The server must decrypt session parameters using a secret, derived from the key agreement protocol in the same way as the client. Then the server must perform the following checks to confirm the protocol's security properties:
1. The server must have the corresponding private key for `receiver_address`, otherwise there is no way to perform the key agreement protocol.
2. `SHA-256(aes_params) == SHA-256(D(E(aes_params)))`, otherwise the key agreement protocol has failed and `secret` is not equal on both sides.

If any of these checks fail, server will immediately drop the connection without responding to the client. If all checks pass, the server must issue an empty datagram (see the Datagram section) to the client in order to prove that it owns the private key for the specified `receiver_address`.


### Datagram

Both the client and server must initialize two AES-CTR instances each, for both TX and RX directions. AES-256 must be used in CTR mode with a 128-bit big-endian counter. Each AES instance is initialized using a (key, nonce) pair belonging to it, which can be taken from `aes_params` in the handshake.

To send a datagram, a peer (the client or server) must build the following structure, encrypt it and send to the other peer:

| Parameter | Size                 | Notes                                                      |
|-----------|----------------------|------------------------------------------------------------|
| length    | 4 bytes (LE)         | Length of the whole datagram, excluding `length` field     |
| nonce     | 32 bytes             | Random value                                               |
| buffer    | `length - 64` bytes  | Actual data to be sent to the other side                   |
| hash      | 32 bytes             | `SHA-256(nonce \|\| buffer)` to ensure integrity             |

The whole structure must be encrypted using the corresponding AES instance (TX for client -> server, RX for server -> client).

The receiving peer must fetch the first 4 bytes, decrypt it into the `length` field and read exactly `length` bytes to get the full datagram. The receiving peer may start to decrypt and process `buffer` earlier, but it must take into account that it may be corrupted, intentionally or occasionally. Datagram `hash` must be checked to ensure the integrity of the `buffer`. In case of failure, no new datagrams can be issued and the connection must be dropped.

The first datagram in the session always goes from the server to the client after a handshake packet was successfully accepted by the server and it's actual buffer is empty. The client should decrypt it and disconnect from the server in case of failure, because it means that the server has not followed the protocol properly and the actual session keys differs on the server and client side.

### Communication details

If you want to dive into communication details, you could check article [ADNL TCP - Liteserver](/docs/develop/network/adnl-tcp) to see some examples.

### Security considerations
#### Handshake padding
It is unknown why the initial TON team decided to include this field into the handshake. `aes_params` integrity is protected by a SHA-256 hash and confidentiality is protected by the key derived from the `secret` parameter. Probably, it was intended to migrate from AES-CTR at some point. To do this, specification may be extended to include a special magic value in `aes_params`, which will signal that the peer is ready to use the updated primitives. The response to such a handshake may be decrypted twice, with new and old schemes, to clarify which scheme the other peer is actually using.

#### Session parameters encryption key derivation process

If an encryption key is derived only from the `secret` parameter, it will be static because the secret is static. To derive a new encryption key for each session, developers also use `SHA-256(aes_params)`, which is random if `aes_params` is random. However, the actual key derivation algorithm with the concatenation of different subarrays is considered harmful.

#### Datagram nonce
It is not obvious why the `nonce` field in the datagram is present because, even without it, any two ciphertexts will differ because of the session-bounded keys for AES and encryption in CTR mode. However, the following attack can be performed in the case of an absent or predictable nonce. CTR encryption mode turns block ciphers, such as AES, into stream ciphers to make it possible to perform a bit-flipping attack. If the attacker knows the plaintext which belongs to encrypted datagram, they can obtain a pure keystream, XOR it with their own plaintext and efficiently replace the message which was sent by peer. The buffer integrity is protected by a SHA-256 hash, but an attacker can replace it too because having knowledge of a full plaintext means having knowledge of its hash. The nonce field is present to prevent such an attack, so no attacker can replace the SHA-256 without having knowledge of the nonce.

## P2P protocol (ADNL over UDP)

Detailed description can be found in article [ADNL UDP - Internode](/docs/develop/network/adnl-udp).

## References
- [The Open Network, p. 80](https://ton.org/ton.pdf)
- [ADNL implementation in TON](https://github.com/ton-blockchain/ton/tree/master/adnl)

_Thanks to the [hacker-volodya](https://github.com/hacker-volodya) for contributing to the community!_  
_Here a [link to the original article](https://github.com/tonstack/ton-docs/tree/main/ADNL) on GitHub._