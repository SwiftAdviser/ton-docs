# TL-B Overview

:::caution advanced level
This information is **very low-level** and could be hard to understand for newcomers.  
So feel free to read about it later.
:::

TL-B stands for "Typed Language - Binary". It is used to describe a scheme of (de)serialization of objects to [cells](/learn/overviews/cells.md). Here are detailed and complete TL-B schemes for all objects in TON: https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb.

## Scheme

Each TL-B scheme consists of declarations. Each declaration describes a _constructor_ for some _type_. For instance, a Bool _type_ may have two _constructors_ for `true` and `false` values.

Typical TL-B declarations are shown below:
```tlb
bool_false$0 = Bool;
bool_true$1 = Bool;

unary_zero$0 = Unary ~0;
unary_succ$1 {n:#} x:(Unary ~n) = Unary ~(n + 1);

acc_trans#5 account_addr:bits256
   transactions:(HashmapAug 64 ^Transaction CurrencyCollection)
   state_update:^(HASH_UPDATE Account)
   = AccountBlock;
```


Each TL-B declaration consist of:
* Constructor: a _constructor name_ immediately followed by an optional _constructor tag_
* a list of explicit and implicit field definitions that are separated by whitespaces (`" "`, `"\n"`, etc)
* sign `=`
* (optionally parametrized) _Type name_

Example: two constructors (with different binary prefixes) for a `Bool` type.
```tlb
bool_false$0 = Bool;
bool_true$1 = Bool;
```

### Constructor
A constructor is declared via a `constructor_name[separator,tag]`.

A `constructor_name` consists of `[A-z0-9_]` symbols. snake_case names are conventionally used.

A constructor name can be followed by a `separator`. The absence of a `separator` means that the `tag` will be calculated automatically as a 32bit  `CRC32`-sum of constructor declarations. If a `separator` is present, it can take two values `#` and `$`. The former means that a `tag` will be given in a hexadecimal form, the latter means a binary `tag`.
After both separators, there may be an underscore symbol `_` which stands for an empty tag.


There is also a special constructor_name `_` (called 'anonymous constructor') which means that there is only one unnamed constructor with an empty tag for a given type.

The table below displays possible tag definitions.

| Constructor | tag |
| ----------- | ----------- |
|  `_`     | empty tag for anonymous constructor     |
|  `some`     | automatically calculated 32-bit tag       |
|  `some#bba`     | 12-bit tag equal to `0b101110111010`      |
|  `some$01011`     | 5-bit tag equal to `0b01011`      |
|  `some#_`     | empty tag      |
|  `some$_`     | empty tag      |

Note that pregenerated tages are not usually used; explicitly declared are preferred.
### Field definitions
#### Explicit
Each field definition has the _ident : type-expr_, where _ident_ is an identifier for the name of the field (replaced by an underscore `_` for anonymous fields) and _type-expr_ is the field type. The type provided here is a type expression, which may include simple types or parametrized types with suitable parameters. Variables — i.e., the (identifiers of the) previously defined fields of types `#` (natural numbers) or `Type` (type of types) — may be used as parameters for the parametrized types.

There are a few predefined _types_:
* `#` - means an unsigned 32-bit number
* `## N` - the same as `uintN` - means an unsigned N-bit number
* `#<= N` - means a number between `0` and `N` (including both). Such a number is stored in `ceil(log2(N+1))` bits.
* `N * Bit` - means N-bit slice
* `^Cell` - means an arbitrary cell in reference
* `^[ field_definitions ]` - means that field definitions are stored in the referenced cell
* `Type` - stands for arbitrary type (but only presents in implicit definitions).

_type-expr_ usually consist of (optionally parametrized) _Type_ only as: `last_trans_lt:uint64` or `_:StateInit`. However, it is possilbe that _type-expr_ also contains conditions. In that case, _type-expr_ consist of _ident_, `:`, _condition_, `?`, _type_. If a condition (which can refer to previously defined fields) renders to `false`, the corresponding field is not presented. For instance `prev:n?^(ProofChain n)` means that `prev` field is only presented for objects when `n>0`.

#### Implicit
Some fields may be implicit. Their definitions are surrounded by curly brackets, which indicate that the field is not actually present in the serialization, but that its value must be deduced from some other data (usually the parameters of the type being serialized).
For instance 
```tlb
nothing$0 {X:Type} = Maybe X;
just$1 {X:Type} value:X = Maybe X;
```

means the following: some other constructor may define the field `var:(Maybe #)`. In that case, the variable will be serialized either as `1` bit and a serialization of `#` (uint32) if `var` is present or as `0` bit if `var` is absent. That way `Maybe` is declared as a C++-like _template_ type for arbitrary type X. However, if `Maybe` is declared as `nothing$0 {X:#} = Maybe X;`, that will mean that `Maybe` is declared for an arbitrary number (not totally arbitrary type X).

### Type definition
A type name consist of `[A-z0-9_]` symbols. By convention it is a CamelCase name.

It can be parametrized by one or more parameters.

Some occurrences of “variables” are prefixed by a tilde (`~`). This means that, prior to deserialization, the exact value of that variable is not known, but instead will be computed during deserialization.

Let's consider:
```tlb
unary_zero$0 = Unary ~0;
unary_succ$1 {n:#} x:(Unary ~n) = Unary ~(n + 1);
```

and the case when we want to deserialize the `Unary ~N` object from the slice containing `0b1111111100101` bit string. When we say that we want to deserialize `Unary ~N`, this means that we do not know yet whether we deserialize `Unary 0`, `Unary 7` or `Unary 1020`. Instead we start with `0b1111111100101` and compare it with the constructor prefixes `0b0` for `unary_zero` and `0b1` for `unary_succ`. We see that we have `unary_succ`, but again the value of `N` cannot be deducted, instead we should obtain it from the deserialization of variable `x`. This variable has type `Unary ~(N-1)` and the value of `N-1` can be deducted from the deserialization of the remaining bits in the slice.
We get the remaining bits of the slice and try to deserialize `Unary ~(N-1)` and again see the `unary_succ` tag. That way we recursively dive into `Unary` until we get to the `Unary ~(N-8)`. At that level we see that the rest of the slice starts from `unary_zero` tag and thus constitutes a `Unary 0` object. Popping back up we can see that we initially had a `Unary 8` object.
So after the deserialization of `Unary ~N` from Slice(`0b1111111100101`) we get a `Unary 8` object and the remaining slice(`0b0101`) from which subsequent variables of the constructor can be deserialized.

### Constraints
Some implicit fields may contain constraints, for instance `{n <= m}`. It means that the previously defined variables n and m should satisfy the corresponding inequality. This inequality is an inherent property of the constructor. It should be checked during serialization and objects with variables which do not satisfy these constraints are invalid.

An example of constructors with constraints:
```tlb
hml_short$0 {m:#} {n:#} len:(Unary ~n) {n <= m} s:(n * Bit) = HmLabel ~n m;
hml_long$10 {m:#} n:(#<= m) s:(n * Bit) = HmLabel ~n m;
hml_same$11 {m:#} v:Bit n:(#<= m) = HmLabel ~n m;
```

## Comments
TL-B schemas support C-like comments:
```tlb
/* 
This is a
multiline
comment 
*/

// This is one line comment
```


## (De)serialization
Given the TL-B scheme, any object can be serialized to builder and deserialized from the slice.
In particular, when we deserialize an object we need to start with the determination of the corresponding constructor using a tag and then deserialize variables one by one from left to right (recursively jumping to the serialization of variables which are TL-B objects themselves).
During serialization we go the other way, by finding and writing to the builder `tag` which corresponds to a given object of that type and then continue from left to right with each variable.

For parsers, it is recommended to read the scheme once and generate a serializator and deserializator for each type, instead of referring to the scheme on the fly.

## BNF grammar

The **Backus–Naur form** can be found at [TlbParser.bnf](https://github.com/andreypfau/intellij-ton/blob/main/src/main/grammars/TlbParser.bnf), thanks to [@andreypfau](https://github.com/andreypfau).

TL-B is also supported by [intellij-ton plugin](https://github.com/andreypfau/intellij-ton).

Docs on TL-B can be found in the [TVM Whitepaper](https://ton.org/tvm.pdf) and in a concise (they have been collected in one place) format [here](https://github.com/tonstack/TL-B-docs).

## Generator of serializators and deserializators
An example of a generator used by a TON node can be found in the [Ton node sources](https://github.com/ton-blockchain/ton/blob/master/crypto/tl/tlbc.cpp).

## What's next?

If you want to know more about TL-B serialization and see some examples of complex structures parsing, 
you can continue by reading:
* [Deep Dive into TL-B](/docs/develop/data-formats/tl-b)

