# TL

TL (Type Language) is a language for describing data structures.

For structuring useful data, when communicating, [TL schemas](https://github.com/ton-blockchain/ton/tree/master/tl/generate/scheme) are used.

TL operates on 32 bit blocks. Accordingly, the data size in TL must be a multiple of 4 bytes.
If the size of the object is not a multiple of 4, we need to add the required number of zero bytes up to the multiple.

Numbers are always encoded in Little Endian order.

More details about TL can be found in [Telegram documentation](https://core.telegram.org/mtproto/TL)

## Encoding bytes array
To encode an array of bytes, we first need to determine its size.
If it is less than 254 bytes, then the encoding with 1 byte as the size is used. If more,
then 0xFE is written as the first byte, as an indicator of a large array, and after it 3 bytes of size follow.

For example, we encode the array `[0xAA, 0xBB]`, its size is 2. We use 1 byte
size and then write the data itself, we get `[0x02, 0xAA, 0xBB]`, done, but we see
that the final size is 3 and not a multiple of 4 bytes, then we need to add 1 byte of padding to make it 4. Result: `[0x02, 0xAA, 0xBB, 0x00]`.

In case we need to encode an array whose size will be equal to, for example, 396,
we do this: 396 >= 254, so we use 3 bytes for size encoding and 1 byte oversize indicator,
we get: `[0xFE, 0x8C, 0x01, 0x00, array bytes]`, 396+4 = 400, which is a multiple of 4, no need to align.

## Non-obvious serialization rules

Often, a 4-byte prefix is written before the schema itself - its ID. The schema ID is a CRC32 with an IEEEE table from the schema text, while symbols such as `;` and brackets `()` are previously removed from the text. The serialization of a schema with an ID prefix is called **boxed**, this allows the parser to determine which schema comes before it if there are multiple options.

How to determine whether to serialize as boxed or not? If our schema is part of another schema, then we need to look at how the field type is specified, if it is specified explicitly, then we serialize without a prefix, if not explicitly (there are many such types), then we need to serialize as boxed. Example:
```tlb
pub.unenc data:bytes = PublicKey;
pub.ed25519 key:int256 = PublicKey;
pub.aes key:int256 = PublicKey;
pub.overlay name:bytes = PublicKey;
```
We have such types, if `PublicKey` is specified in the schema, for example `adnl.node id:PublicKey addr_list:adnl.addressList = adnl.Node`, then it is not explicitly specified and we need to serialize with an ID prefix (boxed). And if it were specified like this: `adnl.node id:pub.ed25519 addr_list:adnl.addressList = adnl.Node`, then it would be explicit, and the prefix would not be needed.

## References

_Here a [link to the original article](https://github.com/xssnick/ton-deep-doc/blob/master/TL.md) by [Oleg Baranov](https://github.com/xssnick)._