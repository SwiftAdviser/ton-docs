# TVM Instructions

:::caution advanced level
This information is **very low-level** and could be hard to understand for newcomers.  
So feel free to read about it later.
:::

## 1 Introduction
This document provides a list of TVM instructions along with their opcodes and mnemonics.

:::tip
[**Here**](https://ton.org/tvm.pdf) is a full description of TON Virtual Machine.
:::

Fift is a stack-based programming language designed to manage TON smart contracts. The Fift assembler is a Fift library that converts mnemonics of TVM instructions into their binary representation.

A description of Fift, including an introduction to the Fift assembler, can be found [here](https://github.com/Piterden/TON-docs/blob/master/Fift.%20A%20Brief%20Introduction.md).

This document specifies the corresponding mnemonic for each instruction. Note the following:

1. Fift is a stack-based language, therefore all the arguments of any instruction are written before it (e.g. [`5 PUSHINT`](#instr-pushint-4), [`s0 s4 XCHG`](#instr-xchg-ij)).
2. Stack registers are denoted by `s0, s1, ..., s15`. Other stack registers (up to 255) are denoted by `i s()` (e.g. `100 s()`).
3. Control registers are denoted by `c0, c1, ..., c15`.

### 1.1 Gas prices
The gas price of each instruction is specified in this document. The basic gas price of an instruction is `10 + b`, where `b` is the instruction length in bits. Some operations have additional fees:
1. _Parsing cells_: Transforming a cell into a slice costs **100 gas units** if the cell is loading for the first time and **25** for subsequent loads during the same transaction. For such instructions, two gas prices are specified (e.g. [`CTOS`](#instr-ctos): `118/43`).
2. _Cell creation_: **500 gas units**.
3. _Throwing exceptions_: **50 gas units**. In this document the exception fee is only specified for an instruction if its primary purpose is to throw (e.g. [`THROWIF`](#instr-throwif-short), [`FITS`](#instr-fits)). If the instruction only throws in some cases, two gas prices are specified (e.g. [`FITS`](#instr-fits): `26/76`).
4. _Tuple creation_: **1 gas unit** for every tuple element.
5. _Implicit jumps_: **10 gas units** for an implicit jump, **5 gas units** for an implicit back jump. This fee is not a part of any instruction.
6. _Moving stack elements between continuations_: **1 gas unit** per element, however moving the first 32 elements is free.

### 1.2 CSV table
A machine-readable list of TVM instructions is available [here](https://github.com/ton-community/ton-docs/blob/main/docs/learn/tvm-instructions/instructions.csv).

## 2 Stack manipulation primitives
Here `0 <= i,j,k <= 15` if not stated otherwise.

### 2.1 Basic stack manipulation primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`00`** | `NOP` | _`-`_ | Does nothing. | `18` |
| **`01`** | `SWAP` | _`x y - y x`_ | Same as [`s1 XCHG0`](#instr-xchg-0i). | `18` |
| **`0i`** | `s[i] XCHG0` |  | Interchanges `s0` with `s[i]`, `1 <= i <= 15`. | `18` |
| **`10ij`** | `s[i] s[j] XCHG` |  | Interchanges `s[i]` with `s[j]`, `1 <= i < j <= 15`. | `26` |
| **`11ii`** | `s0 [ii] s() XCHG` |  | Interchanges `s0` with `s[ii]`, `0 <= ii <= 255`. | `26` |
| **`1i`** | `s1 s[i] XCHG` |  | Interchanges `s1` with `s[i]`, `2 <= i <= 15`. | `18` |
| **`2i`** | `s[i] PUSH` |  | Pushes a copy of the old `s[i]` into the stack. | `18` |
| **`20`** | `DUP` | _`x - x x`_ | Same as [`s0 PUSH`](#instr-push). | `18` |
| **`21`** | `OVER` | _`x y - x y x`_ | Same as [`s1 PUSH`](#instr-push). | `18` |
| **`3i`** | `s[i] POP` |  | Pops the old `s0` value into the old `s[i]`. Equivalent to [`s[i] XCHG0`](#instr-xchg-0i) [`DROP`](#instr-drop) | `18` |
| **`30`** | `DROP` | _`x -`_ | Same as [`s0 POP`](#instr-pop), discards the top-of-stack value. | `18` |
| **`31`** | `NIP` | _`x y - y`_ | Same as [`s1 POP`](#instr-pop). | `18` |
### 2.2 Complex stack manipulation primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`4ijk`** | `s[i] s[j] s[k] XCHG3` |  | Equivalent to [`s2 s[i] XCHG`](#instr-xchg-ij) [`s1 s[j] XCHG`](#instr-xchg-ij) [`s[k] XCHG0`](#instr-xchg-0i). | `26` |
| **`50ij`** | `s[i] s[j] XCHG2` |  | Equivalent to [`s1 s[i] XCHG`](#instr-xchg-ij) [`s[j] XCHG0`](#instr-xchg-0i). | `26` |
| **`51ij`** | `s[i] s[j] XCPU` |  | Equivalent to [`s[i] XCHG0`](#instr-xchg-0i) [`s[j] PUSH`](#instr-push). | `26` |
| **`52ij`** | `s[i] s[j-1] PUXC` |  | Equivalent to [`s[i] PUSH`](#instr-push) [`SWAP`](#instr-swap) [`s[j] XCHG0`](#instr-xchg-0i). | `26` |
| **`53ij`** | `s[i] s[j] PUSH2` |  | Equivalent to [`s[i] PUSH`](#instr-push) [`s[j+1] PUSH`](#instr-push). | `26` |
| **`540ijk`** | `s[i] s[j] s[k] XCHG3_l` |  | Long form of [`XCHG3`](#instr-xchg3). | `34` |
| **`541ijk`** | `s[i] s[j] s[k] XC2PU` |  | Equivalent to [`s[i] s[j] XCHG2`](#instr-xchg2) [`s[k] PUSH`](#instr-push). | `34` |
| **`542ijk`** | `s[i] s[j] s[k-1] XCPUXC` |  | Equivalent to [`s1 s[i] XCHG`](#instr-xchg-ij) [`s[j] s[k-1] PUXC`](#instr-puxc). | `34` |
| **`543ijk`** | `s[i] s[j] s[k] XCPU2` |  | Equivalent to [`s[i] XCHG0`](#instr-xchg-0i) [`s[j] s[k] PUSH2`](#instr-push2). | `34` |
| **`544ijk`** | `s[i] s[j-1] s[k-1] PUXC2` |  | Equivalent to [`s[i] PUSH`](#instr-push) [`s2 XCHG0`](#instr-xchg-0i) [`s[j] s[k] XCHG2`](#instr-xchg2). | `34` |
| **`545ijk`** | `s[i] s[j-1] s[k-1] PUXCPU` |  | Equivalent to [`s[i] s[j-1] PUXC`](#instr-puxc) [`s[k] PUSH`](#instr-push). | `34` |
| **`546ijk`** | `s[i] s[j-1] s[k-2] PU2XC` |  | Equivalent to [`s[i] PUSH`](#instr-push) [`SWAP`](#instr-swap) [`s[j] s[k-1] PUXC`](#instr-puxc). | `34` |
| **`547ijk`** | `s[i] s[j] s[k] PUSH3` |  | Equivalent to [`s[i] PUSH`](#instr-push) [`s[j+1] s[k+1] PUSH2`](#instr-push2). | `34` |
| **`55ij`** | `[i+1] [j+1] BLKSWAP` |  | Permutes two blocks `s[j+i+1] … s[j+1]` and `s[j] … s0`.<br/>`0 <= i,j <= 15`<br/>Equivalent to [`[i+1] [j+1] REVERSE`](#instr-reverse) [`[j+1] 0 REVERSE`](#instr-reverse) [`[i+j+2] 0 REVERSE`](#instr-reverse). | `26` |
| **`5513`** | `ROT2`<br/>`2ROT` | _`a b c d e f - c d e f a b`_ | Rotates the three topmost pairs of stack entries. | `26` |
| **`550i`** | `[i+1] ROLL` |  | Rotates the top `i+1` stack entries.<br/>Equivalent to [`1 [i+1] BLKSWAP`](#instr-blkswap). | `26` |
| **`55i0`** | `[i+1] -ROLL`<br/>`[i+1] ROLLREV` |  | Rotates the top `i+1` stack entries in the other direction.<br/>Equivalent to [`[i+1] 1 BLKSWAP`](#instr-blkswap). | `26` |
| **`56ii`** | `[ii] s() PUSH` |  | Pushes a copy of the old `s[ii]` into the stack.<br/>`0 <= ii <= 255` | `26` |
| **`57ii`** | `[ii] s() POP` |  | Pops the old `s0` value into the old `s[ii]`.<br/>`0 <= ii <= 255` | `26` |
| **`58`** | `ROT` | _`a b c - b c a`_ | Equivalent to [`1 2 BLKSWAP`](#instr-blkswap) or to [`s2 s1 XCHG2`](#instr-xchg2). | `18` |
| **`59`** | `ROTREV`<br/>`-ROT` | _`a b c - c a b`_ | Equivalent to [`2 1 BLKSWAP`](#instr-blkswap) or to [`s2 s2 XCHG2`](#instr-xchg2). | `18` |
| **`5A`** | `SWAP2`<br/>`2SWAP` | _`a b c d - c d a b`_ | Equivalent to [`2 2 BLKSWAP`](#instr-blkswap) or to [`s3 s2 XCHG2`](#instr-xchg2). | `18` |
| **`5B`** | `DROP2`<br/>`2DROP` | _`a b - `_ | Equivalent to [`DROP`](#instr-drop) [`DROP`](#instr-drop). | `18` |
| **`5C`** | `DUP2`<br/>`2DUP` | _`a b - a b a b`_ | Equivalent to [`s1 s0 PUSH2`](#instr-push2). | `18` |
| **`5D`** | `OVER2`<br/>`2OVER` | _`a b c d - a b c d a b`_ | Equivalent to [`s3 s2 PUSH2`](#instr-push2). | `18` |
| **`5Eij`** | `[i+2] [j] REVERSE` |  | Reverses the order of `s[j+i+1] … s[j]`. | `26` |
| **`5F0i`** | `[i] BLKDROP` |  | Equivalent to [`DROP`](#instr-drop) performed `i` times. | `26` |
| **`5Fij`** | `[i] [j] BLKPUSH` |  | Equivalent to `PUSH s(j)` performed `i` times.<br/>`1 <= i <= 15`, `0 <= j <= 15`. | `26` |
| **`60`** | `PICK`<br/>`PUSHX` |  | Pops integer `i` from the stack, then performs [`s[i] PUSH`](#instr-push). | `18` |
| **`61`** | `ROLLX` |  | Pops integer `i` from the stack, then performs [`1 [i] BLKSWAP`](#instr-blkswap). | `18` |
| **`62`** | `-ROLLX`<br/>`ROLLREVX` |  | Pops integer `i` from the stack, then performs [`[i] 1 BLKSWAP`](#instr-blkswap). | `18` |
| **`63`** | `BLKSWX` |  | Pops integers `i`,`j` from the stack, then performs [`[i] [j] BLKSWAP`](#instr-blkswap). | `18` |
| **`64`** | `REVX` |  | Pops integers `i`,`j` from the stack, then performs [`[i] [j] REVERSE`](#instr-reverse). | `18` |
| **`65`** | `DROPX` |  | Pops integer `i` from the stack, then performs [`[i] BLKDROP`](#instr-blkdrop). | `18` |
| **`66`** | `TUCK` | _`a b - b a b`_ | Equivalent to [`SWAP`](#instr-swap) [`OVER`](#instr-over) or to [`s1 s1 XCPU`](#instr-xcpu). | `18` |
| **`67`** | `XCHGX` |  | Pops integer `i` from the stack, then performs [`s[i] XCHG`](#instr-xchg-ij). | `18` |
| **`68`** | `DEPTH` | _`- depth`_ | Pushes the current depth of the stack. | `18` |
| **`69`** | `CHKDEPTH` | _`i -`_ | Pops integer `i` from the stack, then checks whether there are at least `i` elements, generating a stack underflow exception otherwise. | `18/58` |
| **`6A`** | `ONLYTOPX` |  | Pops integer `i` from the stack, then removes all but the top `i` elements. | `18` |
| **`6B`** | `ONLYX` |  | Pops integer `i` from the stack, then leaves only the bottom `i` elements. Approximately equivalent to [`DEPTH`](#instr-depth) [`SWAP`](#instr-swap) [`SUB`](#instr-sub) [`DROPX`](#instr-dropx). | `18` |
| **`6Cij`** | `[i] [j] BLKDROP2` |  | Drops `i` stack elements under the top `j` elements.<br/>`1 <= i <= 15`, `0 <= j <= 15`<br/>Equivalent to [`[i+j] 0 REVERSE`](#instr-reverse) [`[i] BLKDROP`](#instr-blkdrop) [`[j] 0 REVERSE`](#instr-reverse). | `26` |

## 3 Tuple, List, and Null primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`6D`** | `NULL`<br/>`PUSHNULL` | _` - null`_ | Pushes the only value of type _Null_. | `18` |
| **`6E`** | `ISNULL` | _`x - ?`_ | Checks whether `x` is a _Null_, and returns `-1` or `0` accordingly. | `18` |
| **`6F0n`** | `[n] TUPLE` | _`x_1 ... x_n - t`_ | Creates a new _Tuple_ `t=(x_1, … ,x_n)` containing `n` values `x_1`,..., `x_n`.<br/>`0 <= n <= 15` | `26+n` |
| **`6F00`** | `NIL` | _`- t`_ | Pushes the only _Tuple_ `t=()` of length zero. | `26` |
| **`6F01`** | `SINGLE` | _`x - t`_ | Creates a singleton `t:=(x)`, i.e., a _Tuple_ of length one. | `27` |
| **`6F02`** | `PAIR`<br/>`CONS` | _`x y - t`_ | Creates pair `t:=(x,y)`. | `28` |
| **`6F03`** | `TRIPLE` | _`x y z - t`_ | Creates triple `t:=(x,y,z)`. | `29` |
| **`6F1k`** | `[k] INDEX` | _`t - x`_ | Returns the `k`-th element of a _Tuple_ `t`.<br/>`0 <= k <= 15`. | `26` |
| **`6F10`** | `FIRST`<br/>`CAR` | _`t - x`_ | Returns the first element of a _Tuple_. | `26` |
| **`6F11`** | `SECOND`<br/>`CDR` | _`t - y`_ | Returns the second element of a _Tuple_. | `26` |
| **`6F12`** | `THIRD` | _`t - z`_ | Returns the third element of a _Tuple_. | `26` |
| **`6F2n`** | `[n] UNTUPLE` | _`t - x_1 ... x_n`_ | Unpacks a _Tuple_ `t=(x_1,...,x_n)` of length equal to `0 <= n <= 15`.<br/>If `t` is not a _Tuple_, or if `\|t\| != n`, a type check exception is thrown. | `26+n` |
| **`6F21`** | `UNSINGLE` | _`t - x`_ | Unpacks a singleton `t=(x)`. | `27` |
| **`6F22`** | `UNPAIR`<br/>`UNCONS` | _`t - x y`_ | Unpacks a pair `t=(x,y)`. | `28` |
| **`6F23`** | `UNTRIPLE` | _`t - x y z`_ | Unpacks a triple `t=(x,y,z)`. | `29` |
| **`6F3k`** | `[k] UNPACKFIRST` | _`t - x_1 ... x_k`_ | Unpacks first `0 <= k <= 15` elements of a _Tuple_ `t`.<br/>If `\|t\|<k`, throws a type check exception. | `26+k` |
| **`6F30`** | `CHKTUPLE` | _`t -`_ | Checks whether `t` is a _Tuple_. If not, throws a type check exception. | `26` |
| **`6F4n`** | `[n] EXPLODE` | _`t - x_1 ... x_m m`_ | Unpacks a _Tuple_ `t=(x_1,...,x_m)` and returns its length `m`, but only if `m <= n <= 15`. Otherwise throws a type check exception. | `26+m` |
| **`6F5k`** | `[k] SETINDEX` | _`t x - t'`_ | Computes _Tuple_ `t'` that differs from `t` only at position `t'_{k+1}`, which is set to `x`.<br/>`0 <= k <= 15`<br/>If `k >= \|t\|`, throws a range check exception. | `26+\|t\|` |
| **`6F50`** | `SETFIRST` | _`t x - t'`_ | Sets the first component of _Tuple_ `t` to `x` and returns the resulting _Tuple_ `t'`. | `26+\|t\|` |
| **`6F51`** | `SETSECOND` | _`t x - t'`_ | Sets the second component of _Tuple_ `t` to `x` and returns the resulting _Tuple_ `t'`. | `26+\|t\|` |
| **`6F52`** | `SETTHIRD` | _`t x - t'`_ | Sets the third component of _Tuple_ `t` to `x` and returns the resulting _Tuple_ `t'`. | `26+\|t\|` |
| **`6F6k`** | `[k] INDEXQ` | _`t - x`_ | Returns the `k`-th element of a _Tuple_ `t`, where `0 <= k <= 15`. In other words, returns `x_{k+1}` if `t=(x_1,...,x_n)`. If `k>=n`, or if `t` is _Null_, returns a _Null_ instead of `x`. | `26` |
| **`6F60`** | `FIRSTQ`<br/>`CARQ` | _`t - x`_ | Returns the first element of a _Tuple_. | `26` |
| **`6F61`** | `SECONDQ`<br/>`CDRQ` | _`t - y`_ | Returns the second element of a _Tuple_. | `26` |
| **`6F62`** | `THIRDQ` | _`t - z`_ | Returns the third element of a _Tuple_. | `26` |
| **`6F7k`** | `[k] SETINDEXQ` | _`t x - t'`_ | Sets the `k`-th component of _Tuple_ `t` to `x`, where `0 <= k < 16`, and returns the resulting _Tuple_ `t'`.<br/>If `\|t\| <= k`, first extends the original _Tuple_ to length `n’=k+1` by setting all new components to _Null_. If the original value of `t` is _Null_, treats it as an empty _Tuple_. If `t` is not _Null_ or _Tuple_, throws an exception. If `x` is _Null_ and either `\|t\| <= k` or `t` is _Null_, then always returns `t'=t` (and does not consume tuple creation gas). | `26+\|t’\|` |
| **`6F70`** | `SETFIRSTQ` | _`t x - t'`_ | Sets the first component of _Tuple_ `t` to `x` and returns the resulting _Tuple_ `t'`. | `26+\|t’\|` |
| **`6F71`** | `SETSECONDQ` | _`t x - t'`_ | Sets the second component of _Tuple_ `t` to `x` and returns the resulting _Tuple_ `t'`. | `26+\|t’\|` |
| **`6F72`** | `SETTHIRDQ` | _`t x - t'`_ | Sets the third component of _Tuple_ `t` to `x` and returns the resulting _Tuple_ `t'`. | `26+\|t’\|` |
| **`6F80`** | `TUPLEVAR` | _`x_1 ... x_n n - t`_ | Creates a new _Tuple_ `t` of length `n` similarly to [`TUPLE`](#instr-tuple), but with `0 <= n <= 255` taken from the stack. | `26+n` |
| **`6F81`** | `INDEXVAR` | _`t k - x`_ | Similar to [`k INDEX`](#instr-index), but with `0 <= k <= 254` taken from the stack. | `26` |
| **`6F82`** | `UNTUPLEVAR` | _`t n - x_1 ... x_n`_ | Similar to [`n UNTUPLE`](#instr-untuple), but with `0 <= n <= 255` taken from the stack. | `26+n` |
| **`6F83`** | `UNPACKFIRSTVAR` | _`t n - x_1 ... x_n`_ | Similar to [`n UNPACKFIRST`](#instr-unpackfirst), but with `0 <= n <= 255` taken from the stack. | `26+n` |
| **`6F84`** | `EXPLODEVAR` | _`t n - x_1 ... x_m m`_ | Similar to [`n EXPLODE`](#instr-explode), but with `0 <= n <= 255` taken from the stack. | `26+m` |
| **`6F85`** | `SETINDEXVAR` | _`t x k - t'`_ | Similar to [`k SETINDEX`](#instr-setindex), but with `0 <= k <= 254` taken from the stack. | `26+\|t’\|` |
| **`6F86`** | `INDEXVARQ` | _`t k - x`_ | Similar to [`n INDEXQ`](#instr-indexq), but with `0 <= k <= 254` taken from the stack. | `26` |
| **`6F87`** | `SETINDEXVARQ` | _`t x k - t'`_ | Similar to [`k SETINDEXQ`](#instr-setindexq), but with `0 <= k <= 254` taken from the stack. | `26+\|t’\|` |
| **`6F88`** | `TLEN` | _`t - n`_ | Returns the length of a _Tuple_. | `26` |
| **`6F89`** | `QTLEN` | _`t - n or -1`_ | Similar to [`TLEN`](#instr-tlen), but returns `-1` if `t` is not a _Tuple_. | `26` |
| **`6F8A`** | `ISTUPLE` | _`t - ?`_ | Returns `-1` or `0` depending on whether `t` is a _Tuple_. | `26` |
| **`6F8B`** | `LAST` | _`t - x`_ | Returns the last element of a non-empty _Tuple_ `t`. | `26` |
| **`6F8C`** | `TPUSH`<br/>`COMMA` | _`t x - t'`_ | Appends a value `x` to a _Tuple_ `t=(x_1,...,x_n)`, but only if the resulting _Tuple_ `t'=(x_1,...,x_n,x)` is of length at most 255. Otherwise throws a type check exception. | `26+\|t’\|` |
| **`6F8D`** | `TPOP` | _`t - t' x`_ | Detaches the last element `x=x_n` from a non-empty _Tuple_ `t=(x_1,...,x_n)`, and returns both the resulting _Tuple_ `t'=(x_1,...,x_{n-1})` and the original last element `x`. | `26+\|t’\|` |
| **`6FA0`** | `NULLSWAPIF` | _`x - x or null x`_ | Pushes a _Null_ under the topmost _Integer_ `x`, but only if `x!=0`. | `26` |
| **`6FA1`** | `NULLSWAPIFNOT` | _`x - x or null x`_ | Pushes a _Null_ under the topmost _Integer_ `x`, but only if `x=0`. May be used for stack alignment after quiet primitives such as [`PLDUXQ`](#instr-plduxq). | `26` |
| **`6FA2`** | `NULLROTRIF` | _`x y - x y or null x y`_ | Pushes a _Null_ under the second stack entry from the top, but only if the topmost _Integer_ `y` is non-zero. | `26` |
| **`6FA3`** | `NULLROTRIFNOT` | _`x y - x y or null x y`_ | Pushes a _Null_ under the second stack entry from the top, but only if the topmost _Integer_ `y` is zero. May be used for stack alignment after quiet primitives such as [`LDUXQ`](#instr-lduxq). | `26` |
| **`6FA4`** | `NULLSWAPIF2` | _`x - x or null null x`_ | Pushes two nulls under the topmost _Integer_ `x`, but only if `x!=0`.<br/>Equivalent to [`NULLSWAPIF`](#instr-nullswapif) [`NULLSWAPIF`](#instr-nullswapif). | `26` |
| **`6FA5`** | `NULLSWAPIFNOT2` | _`x - x or null null x`_ | Pushes two nulls under the topmost _Integer_ `x`, but only if `x=0`.<br/>Equivalent to [`NULLSWAPIFNOT`](#instr-nullswapifnot) [`NULLSWAPIFNOT`](#instr-nullswapifnot). | `26` |
| **`6FA6`** | `NULLROTRIF2` | _`x y - x y or null null x y`_ | Pushes two nulls under the second stack entry from the top, but only if the topmost _Integer_ `y` is non-zero.<br/>Equivalent to [`NULLROTRIF`](#instr-nullrotrif) [`NULLROTRIF`](#instr-nullrotrif). | `26` |
| **`6FA7`** | `NULLROTRIFNOT2` | _`x y - x y or null null x y`_ | Pushes two nulls under the second stack entry from the top, but only if the topmost _Integer_ `y` is zero.<br/>Equivalent to [`NULLROTRIFNOT`](#instr-nullrotrifnot) [`NULLROTRIFNOT`](#instr-nullrotrifnot). | `26` |
| **`6FBij`** | `[i] [j] INDEX2` | _`t - x`_ | Recovers `x=(t_{i+1})_{j+1}` for `0 <= i,j <= 3`.<br/>Equivalent to [`[i] INDEX`](#instr-index) [`[j] INDEX`](#instr-index). | `26` |
| **`6FB4`** | `CADR` | _`t - x`_ | Recovers `x=(t_2)_1`. | `26` |
| **`6FB5`** | `CDDR` | _`t - x`_ | Recovers `x=(t_2)_2`. | `26` |
| **`6FE_ijk`** | `[i] [j] [k] INDEX3` | _`t - x`_ | Recovers `x=t_{i+1}_{j+1}_{k+1}`.<br/>`0 <= i,j,k <= 3`<br/>Equivalent to [`[i] [j] INDEX2`](#instr-index2) [`[k] INDEX`](#instr-index). | `26` |
| **`6FD4`** | `CADDR` | _`t - x`_ | Recovers `x=t_2_2_1`. | `26` |
| **`6FD5`** | `CDDDR` | _`t - x`_ | Recovers `x=t_2_2_2`. | `26` |

## 4 Constant or literal primitives
### 4.1 Integer and boolean constants
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`7i`** | `[x] PUSHINT`<br/>`[x] INT` | _`- x`_ | Pushes integer `x` into the stack. `-5 <= x <= 10`.<br/>Here `i` equals four lower-order bits of `x` (`i=x mod 16`). | `18` |
| **`70`** | `ZERO`<br/>`FALSE` | _`- 0`_ |  | `18` |
| **`71`** | `ONE` | _`- 1`_ |  | `18` |
| **`72`** | `TWO` | _`- 2`_ |  | `18` |
| **`7A`** | `TEN` | _`- 10`_ |  | `18` |
| **`7F`** | `TRUE` | _`- -1`_ |  | `18` |
| **`80xx`** | `[xx] PUSHINT`<br/>`[xx] INT` | _`- xx`_ | Pushes integer `xx`. `-128 <= xx <= 127`. | `26` |
| **`81xxxx`** | `[xxxx] PUSHINT`<br/>`[xxxx] INT` | _`- xxxx`_ | Pushes integer `xxxx`. `-2^15 <= xx < 2^15`. | `34` |
| **`82lxxx`** | `[xxx] PUSHINT`<br/>`[xxx] INT` | _`- xxx`_ | Pushes integer `xxx`.<br/>_Details:_ 5-bit `0 <= l <= 30` determines the length `n=8l+19` of signed big-endian integer `xxx`.<br/>The total length of this instruction is `l+4` bytes or `n+13=8l+32` bits. | `23` |
| **`83xx`** | `[xx+1] PUSHPOW2` | _`- 2^(xx+1)`_ | (Quietly) pushes `2^(xx+1)` for `0 <= xx <= 255`.<br/>`2^256` is a `NaN`. | `26` |
| **`83FF`** | `PUSHNAN` | _`- NaN`_ | Pushes a `NaN`. | `26` |
| **`84xx`** | `[xx+1] PUSHPOW2DEC` | _`- 2^(xx+1)-1`_ | Pushes `2^(xx+1)-1` for `0 <= xx <= 255`. | `26` |
| **`85xx`** | `[xx+1] PUSHNEGPOW2` | _`- -2^(xx+1)`_ | Pushes `-2^(xx+1)` for `0 <= xx <= 255`. | `26` |
### 4.2 Constant slices, continuations, cells, and references
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`88`** | `[ref] PUSHREF` | _`- c`_ | Pushes the reference `ref` into the stack.<br/>_Details:_ Pushes the first reference of `cc.code` into the stack as a _Cell_ (and removes this reference from the current continuation). | `18` |
| **`89`** | `[ref] PUSHREFSLICE` | _`- s`_ | Similar to [`PUSHREF`](#instr-pushref), but converts the cell into a _Slice_. | `118/43` |
| **`8A`** | `[ref] PUSHREFCONT` | _`- cont`_ | Similar to [`PUSHREFSLICE`](#instr-pushrefslice), but makes a simple ordinary _Continuation_ out of the cell. | `118/43` |
| **`8Bxsss`** | `[slice] PUSHSLICE`<br/>`[slice] SLICE` | _`- s`_ | Pushes the slice `slice` into the stack.<br/>_Details:_ Pushes the (prefix) subslice of `cc.code` consisting of its first `8x+4` bits and no references (i.e., essentially a bitstring), where `0 <= x <= 15`.<br/>A completion tag is assumed, meaning that all trailing zeroes and the last binary one (if present) are removed from this bitstring.<br/>If the original bitstring consists only of zeroes, an empty slice will be pushed. | `22` |
| **`8Crxxssss`** | `[slice] PUSHSLICE`<br/>`[slice] SLICE` | _`- s`_ | Pushes the slice `slice` into the stack.<br/>_Details:_ Pushes the (prefix) subslice of `cc.code` consisting of its first `1 <= r+1 <= 4` references and up to first `8xx+1` bits of data, with `0 <= xx <= 31`.<br/>A completion tag is also assumed. | `25` |
| **`8Drxxsssss`** | `[slice] PUSHSLICE`<br/>`[slice] SLICE` | _`- s`_ | Pushes the slice `slice` into the stack.<br/>_Details:_ Pushes the subslice of `cc.code` consisting of `0 <= r <= 4` references and up to `8xx+6` bits of data, with `0 <= xx <= 127`.<br/>A completion tag is assumed. | `28` |
|  | `x{} PUSHSLICE`<br/>`x{ABCD1234} PUSHSLICE`<br/>`b{01101} PUSHSLICE` | _`- s`_ | Examples of [`PUSHSLICE`](#instr-pushslice).<br/>`x{}` is an empty slice. `x{...}` is a hexadecimal literal. `b{...}` is a binary literal.<br/>More on slice literals [here](https://github.com/Piterden/TON-docs/blob/master/Fift.%20A%20Brief%20Introduction.md#user-content-51-slice-literals).<br/>Note that the assembler can replace [`PUSHSLICE`](#instr-pushslice) with [`PUSHREFSLICE`](#instr-pushrefslice) in certain situations (e.g. if there’s not enough space in the current continuation). |  |
|  | `<b x{AB12} s, b> PUSHREF`<br/>`<b x{AB12} s, b> PUSHREFSLICE` | _`- c/s`_ | Examples of [`PUSHREF`](#instr-pushref) and [`PUSHREFSLICE`](#instr-pushrefslice).<br/>More on building cells in fift [here](https://github.com/Piterden/TON-docs/blob/master/Fift.%20A%20Brief%20Introduction.md#user-content-52-builder-primitives). |  |
| **`8F_rxxcccc`** | `[builder] PUSHCONT`<br/>`[builder] CONT` | _`- c`_ | Pushes a continuation made from `builder`.<br/>_Details:_ Pushes the simple ordinary continuation `cccc` made from the first `0 <= r <= 3` references and the first `0 <= xx <= 127` bytes of `cc.code`. | `26` |
| **`9xccc`** | `[builder] PUSHCONT`<br/>`[builder] CONT` | _`- c`_ | Pushes a continuation made from `builder`.<br/>_Details:_ Pushes an `x`-byte continuation for `0 <= x <= 15`. | `18` |
|  | `<{ code }> PUSHCONT`<br/>`<{ code }> CONT`<br/>`CONT:<{ code }>` | _`- c`_ | Pushes a continuation with code `code`.<br/>Note that the assembler can replace [`PUSHCONT`](#instr-pushcont) with [`PUSHREFCONT`](#instr-pushrefcont) in certain situations (e.g. if there’s not enough space in the current continuation). |  |

## 5 Arithmetic primitives
### 5.1 Addition, subtraction, multiplication
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`A0`** | `ADD` | _`x y - x+y`_ |  | `18` |
| **`A1`** | `SUB` | _`x y - x-y`_ |  | `18` |
| **`A2`** | `SUBR` | _`x y - y-x`_ | Equivalent to [`SWAP`](#instr-swap) [`SUB`](#instr-sub). | `18` |
| **`A3`** | `NEGATE` | _`x - -x`_ | Equivalent to [`-1 MULCONST`](#instr-mulconst) or to [`ZERO SUBR`](#instr-subr).<br/>Notice that it triggers an integer overflow exception if `x=-2^256`. | `18` |
| **`A4`** | `INC` | _`x - x+1`_ | Equivalent to [`1 ADDCONST`](#instr-addconst). | `18` |
| **`A5`** | `DEC` | _`x - x-1`_ | Equivalent to [`-1 ADDCONST`](#instr-addconst). | `18` |
| **`A6cc`** | `[cc] ADDCONST`<br/>`[cc] ADDINT`<br/>`[-cc] SUBCONST`<br/>`[-cc] SUBINT` | _`x - x+cc`_ | `-128 <= cc <= 127`. | `26` |
| **`A7cc`** | `[cc] MULCONST`<br/>`[cc] MULINT` | _`x - x*cc`_ | `-128 <= cc <= 127`. | `26` |
| **`A8`** | `MUL` | _`x y - x*y`_ |  | `18` |
### 5.2 Division
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`A9mscdf`** |  |  | This is the general encoding of division, with an optional pre-multiplication and an optional replacement of the division or multiplication by a shift. Variable fields are as follows:<br/>`0 <= m <= 1`  -  Indicates whether there is pre-multiplication ([`MULDIV`](#instr-muldiv) and its variants), possibly replaced by a left shift.<br/>`0 <= s <= 2`  -  Indicates whether either the multiplication or the division have been replaced by shifts: `s=0` - no replacement, `s=1` - division replaced by a right shift, `s=2` - multiplication replaced by a left shift (possible only for `m=1`).<br/>`0 <= c <= 1`  -  Indicates whether there is a constant one-byte argument `tt` for the shift operator (if `s!=0`). For `s=0`, `c=0`. If `c=1`, then `0 <= tt <= 255`, and the shift is performed by `tt+1` bits. If `s!=0` and `c=0`, then the shift amount is provided to the instruction as a top-of-stack _Integer_ in range `0...256`.<br/>`1 <= d <= 3`  -  Indicates which results of division are required: `1` - only the quotient, `2` - only the remainder, `3` - both.<br/>`0 <= f <= 2`  -  Rounding mode: `0` - floor, `1` - nearest integer, `2` - ceiling.<br/>All instructions below are variants of this. | `26` |
| **`A904`** | `DIV` | _`x y - q`_ | `q=floor(x/y)`, `r=x-y*q` | `26` |
| **`A905`** | `DIVR` | _`x y - q’`_ | `q’=round(x/y)`, `r’=x-y*q’` | `26` |
| **`A906`** | `DIVC` | _`x y - q''`_ | `q’’=ceil(x/y)`, `r’’=x-y*q’’` | `26` |
| **`A908`** | `MOD` | _`x y - r`_ |  | `26` |
| **`A90C`** | `DIVMOD` | _`x y - q r`_ |  | `26` |
| **`A90D`** | `DIVMODR` | _`x y - q' r'`_ |  | `26` |
| **`A90E`** | `DIVMODC` | _`x y - q'' r''`_ |  | `26` |
| **`A925`** | `RSHIFTR` | _`x y - round(x/2^y)`_ |  | `26` |
| **`A926`** | `RSHIFTC` | _`x y - ceil(x/2^y)`_ |  | `34` |
| **`A935tt`** | `[tt+1] RSHIFTR#` | _`x y - round(x/2^(tt+1))`_ |  | `34` |
| **`A936tt`** | `[tt+1] RSHIFTC#` | _`x y - ceil(x/2^(tt+1))`_ |  | `34` |
| **`A938tt`** | `[tt+1] MODPOW2#` | _`x - x mod 2^(tt+1)`_ |  | `26` |
| **`A98`** | `MULDIV` | _`x y z - q`_ | `q=floor(x*y/z)` | `26` |
| **`A985`** | `MULDIVR` | _`x y z - q'`_ | `q'=round(x*y/z)` | `26` |
| **`A98C`** | `MULDIVMOD` | _`x y z - q r`_ | `q=floor(x*y/z)`, `r=x*y-z*q` | `26` |
| **`A9A4`** | `MULRSHIFT` | _`x y z - floor(x*y/2^z)`_ | `0 <= z <= 256` | `26` |
| **`A9A5`** | `MULRSHIFTR` | _`x y z - round(x*y/2^z)`_ | `0 <= z <= 256` | `26` |
| **`A9A6`** | `MULRSHIFTC` | _`x y z - ceil(x*y/2^z)`_ | `0 <= z <= 256` | `34` |
| **`A9B4tt`** | `[tt+1] MULRSHIFT#` | _`x y - floor(x*y/2^(tt+1))`_ |  | `34` |
| **`A9B5tt`** | `[tt+1] MULRSHIFTR#` | _`x y - round(x*y/2^(tt+1))`_ |  | `34` |
| **`A9B6tt`** | `[tt+1] MULRSHIFTC#` | _`x y - ceil(x*y/2^(tt+1))`_ |  | `26` |
| **`A9C4`** | `LSHIFTDIV` | _`x y z - floor(2^z*x/y)`_ | `0 <= z <= 256` | `26` |
| **`A9C5`** | `LSHIFTDIVR` | _`x y z - round(2^z*x/y)`_ | `0 <= z <= 256` | `26` |
| **`A9C6`** | `LSHIFTDIVC` | _`x y z - ceil(2^z*x/y)`_ | `0 <= z <= 256` | `34` |
| **`A9D4tt`** | `[tt+1] LSHIFT#DIV` | _`x y - floor(2^(tt+1)*x/y)`_ |  | `34` |
| **`A9D5tt`** | `[tt+1] LSHIFT#DIVR` | _`x y - round(2^(tt+1)*x/y)`_ |  | `34` |
| **`A9D6tt`** | `[tt+1] LSHIFT#DIVC` | _`x y - ceil(2^(tt+1)*x/y)`_ |  | `26` |
### 5.3 Shifts, logical operations
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`AAcc`** | `[cc+1] LSHIFT#` | _`x - x*2^(cc+1)`_ | `0 <= cc <= 255` | `26` |
| **`ABcc`** | `[cc+1] RSHIFT#` | _`x - floor(x/2^(cc+1))`_ | `0 <= cc <= 255` | `18` |
| **`AC`** | `LSHIFT` | _`x y - x*2^y`_ | `0 <= y <= 1023` | `18` |
| **`AD`** | `RSHIFT` | _`x y - floor(x/2^y)`_ | `0 <= y <= 1023` | `18` |
| **`AE`** | `POW2` | _`y - 2^y`_ | `0 <= y <= 1023`<br/>Equivalent to [`ONE`](#instr-one) [`SWAP`](#instr-swap) [`LSHIFT`](#instr-lshift-var). | `18` |
| **`B0`** | `AND` | _`x y - x&y`_ | Bitwise and of two signed integers `x` and `y`, sign-extended to infinity. | `18` |
| **`B1`** | `OR` | _`x y - x\|y`_ | Bitwise or of two integers. | `18` |
| **`B2`** | `XOR` | _`x y - x xor y`_ | Bitwise xor of two integers. | `18` |
| **`B3`** | `NOT` | _`x - ~x`_ | Bitwise not of an integer. | `26` |
| **`B4cc`** | `[cc+1] FITS` | _`x - x`_ | Checks whether `x` is a `cc+1`-bit signed integer for `0 <= cc <= 255` (i.e., whether `-2^cc <= x < 2^cc`).<br/>If not, either triggers an integer overflow exception, or replaces `x` with a `NaN` (quiet version). | `26/76` |
| **`B400`** | `CHKBOOL` | _`x - x`_ | Checks whether `x` is a “boolean value'' (i.e., either 0 or -1). | `26/76` |
| **`B5cc`** | `[cc+1] UFITS` | _`x - x`_ | Checks whether `x` is a `cc+1`-bit unsigned integer for `0 <= cc <= 255` (i.e., whether `0 <= x < 2^(cc+1)`). | `26/76` |
| **`B500`** | `CHKBIT` | _`x - x`_ | Checks whether `x` is a binary digit (i.e., zero or one). | `26/76` |
| **`B600`** | `FITSX` | _`x c - x`_ | Checks whether `x` is a `c`-bit signed integer for `0 <= c <= 1023`. | `26/76` |
| **`B601`** | `UFITSX` | _`x c - x`_ | Checks whether `x` is a `c`-bit unsigned integer for `0 <= c <= 1023`. | `26/76` |
| **`B602`** | `BITSIZE` | _`x - c`_ | Computes smallest `c >= 0` such that `x` fits into a `c`-bit signed integer (`-2^(c-1) <= c < 2^(c-1)`). | `26` |
| **`B603`** | `UBITSIZE` | _`x - c`_ | Computes smallest `c >= 0` such that `x` fits into a `c`-bit unsigned integer (`0 <= x < 2^c`), or throws a range check exception. | `26` |
| **`B608`** | `MIN` | _`x y - x or y`_ | Computes the minimum of two integers `x` and `y`. | `26` |
| **`B609`** | `MAX` | _`x y - x or y`_ | Computes the maximum of two integers `x` and `y`. | `26` |
| **`B60A`** | `MINMAX`<br/>`INTSORT2` | _`x y - x y or y x`_ | Sorts two integers. Quiet version of this operation returns two `NaN`s if any of the arguments are `NaN`s. | `26` |
| **`B60B`** | `ABS` | _`x - \|x\|`_ | Computes the absolute value of an integer `x`. | `26` |
### 5.4 Quiet arithmetic primitives
Quiet operations return `NaN` instead of throwing exceptions if one of their arguments is a `NaN` or in the case of an integer overflow.
Quiet operations have a prefix `Q` as shown below. Another way to make an operation quiet is to add `QUIET` before it (i.e. one can write [`QUIET ADD`](#instr-add) instead of [`QADD`](#instr-qadd)).
Quiet versions of integer comparison primitives are also available ([`QUIET SGN`](#instr-sgn), [`QUIET LESS`](#instr-less) etc).

| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`B7A0`** | `QADD` | _`x y - x+y`_ |  | `26` |
| **`B7A1`** | `QSUB` | _`x y - x-y`_ |  | `26` |
| **`B7A2`** | `QSUBR` | _`x y - y-x`_ |  | `26` |
| **`B7A3`** | `QNEGATE` | _`x - -x`_ |  | `26` |
| **`B7A4`** | `QINC` | _`x - x+1`_ |  | `26` |
| **`B7A5`** | `QDEC` | _`x - x-1`_ |  | `26` |
| **`B7A8`** | `QMUL` | _`x y - x*y`_ |  | `26` |
| **`B7A904`** | `QDIV` | _`x y - q`_ | Division returns `NaN` if `y=0`. | `34` |
| **`B7A905`** | `QDIVR` | _`x y - q’`_ |  | `34` |
| **`B7A906`** | `QDIVC` | _`x y - q''`_ |  | `34` |
| **`B7A908`** | `QMOD` | _`x y - r`_ |  | `34` |
| **`B7A90C`** | `QDIVMOD` | _`x y - q r`_ |  | `34` |
| **`B7A90D`** | `QDIVMODR` | _`x y - q' r'`_ |  | `34` |
| **`B7A90E`** | `QDIVMODC` | _`x y - q'' r''`_ |  | `34` |
| **`B7A985`** | `QMULDIVR` | _`x y z - q'`_ |  | `34` |
| **`B7A98C`** | `QMULDIVMOD` | _`x y z - q r`_ |  | `34` |
| **`B7AC`** | `QLSHIFT` | _`x y - x*2^y`_ |  | `26` |
| **`B7AD`** | `QRSHIFT` | _`x y - floor(x/2^y)`_ |  | `26` |
| **`B7AE`** | `QPOW2` | _`y - 2^y`_ |  | `26` |
| **`B7B0`** | `QAND` | _`x y - x&y`_ |  | `26` |
| **`B7B1`** | `QOR` | _`x y - x\|y`_ |  | `26` |
| **`B7B2`** | `QXOR` | _`x y - x xor y`_ |  | `26` |
| **`B7B3`** | `QNOT` | _`x - ~x`_ |  | `26` |
| **`B7B4cc`** | `[cc+1] QFITS` | _`x - x`_ | Replaces `x` with a `NaN` if x is not a `cc+1`-bit signed integer, leaves it intact otherwise. | `34` |
| **`B7B5cc`** | `[cc+1] QUFITS` | _`x - x`_ | Replaces `x` with a `NaN` if x is not a `cc+1`-bit unsigned integer, leaves it intact otherwise. | `34` |
| **`B7B600`** | `QFITSX` | _`x c - x`_ | Replaces `x` with a `NaN` if x is not a c-bit signed integer, leaves it intact otherwise. | `34` |
| **`B7B601`** | `QUFITSX` | _`x c - x`_ | Replaces `x` with a `NaN` if x is not a c-bit unsigned integer, leaves it intact otherwise. | `34` |

## 6 Comparison primitives
### 6.1 Integer comparison
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`B8`** | `SGN` | _`x - sgn(x)`_ | Computes the sign of an integer `x`:<br/>`-1` if `x<0`, `0` if `x=0`, `1` if `x>0`. | `18` |
| **`B9`** | `LESS` | _`x y - x<y`_ | Returns `-1` if `x<y`, `0` otherwise. | `18` |
| **`BA`** | `EQUAL` | _`x y - x=y`_ | Returns `-1` if `x=y`, `0` otherwise. | `18` |
| **`BB`** | `LEQ` | _`x y - x<=y`_ |  | `18` |
| **`BC`** | `GREATER` | _`x y - x>y`_ |  | `18` |
| **`BD`** | `NEQ` | _`x y - x!=y`_ | Equivalent to [`EQUAL`](#instr-equal) [`NOT`](#instr-not). | `18` |
| **`BE`** | `GEQ` | _`x y - x>=y`_ | Equivalent to [`LESS`](#instr-less) [`NOT`](#instr-not). | `18` |
| **`BF`** | `CMP` | _`x y - sgn(x-y)`_ | Computes the sign of `x-y`:<br/>`-1` if `x<y`, `0` if `x=y`, `1` if `x>y`.<br/>No integer overflow can occur here unless `x` or `y` is a `NaN`. | `18` |
| **`C0yy`** | `[yy] EQINT` | _`x - x=yy`_ | Returns `-1` if `x=yy`, `0` otherwise.<br/>`-2^7 <= yy < 2^7`. | `26` |
| **`C000`** | `ISZERO` | _`x - x=0`_ | Checks whether an integer is zero. Corresponds to Forth's `0=`. | `26` |
| **`C1yy`** | `[yy] LESSINT`<br/>`[yy-1] LEQINT` | _`x - x<yy`_ | Returns `-1` if `x<yy`, `0` otherwise.<br/>`-2^7 <= yy < 2^7`. | `26` |
| **`C100`** | `ISNEG` | _`x - x<0`_ | Checks whether an integer is negative. Corresponds to Forth's `0<`. | `26` |
| **`C101`** | `ISNPOS` | _`x - x<=0`_ | Checks whether an integer is non-positive. | `26` |
| **`C2yy`** | `[yy] GTINT`<br/>`[yy+1] GEQINT` | _`x - x>yy`_ | Returns `-1` if `x>yy`, `0` otherwise.<br/>`-2^7 <= yy < 2^7`. | `26` |
| **`C200`** | `ISPOS` | _`x - x>0`_ | Checks whether an integer is positive. Corresponds to Forth's `0>`. | `26` |
| **`C2FF`** | `ISNNEG` | _`x - x >=0`_ | Checks whether an integer is non-negative. | `26` |
| **`C3yy`** | `[yy] NEQINT` | _`x - x!=yy`_ | Returns `-1` if `x!=yy`, `0` otherwise.<br/>`-2^7 <= yy < 2^7`. | `26` |
| **`C4`** | `ISNAN` | _`x - x=NaN`_ | Checks whether `x` is a `NaN`. | `18` |
| **`C5`** | `CHKNAN` | _`x - x`_ | Throws an arithmetic overflow exception if `x` is a `NaN`. | `18/68` |
### 6.2 Other comparison
Most of these "other comparison" primitives actually compare the data portions of _Slices_ as bitstrings (ignoring references if not stated otherwise).

| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`C700`** | `SEMPTY` | _`s - ?`_ | Checks whether a _Slice_ `s` is empty (i.e., contains no bits of data and no cell references). | `26` |
| **`C701`** | `SDEMPTY` | _`s - ?`_ | Checks whether _Slice_ `s` has no bits of data. | `26` |
| **`C702`** | `SREMPTY` | _`s - ?`_ | Checks whether _Slice_ `s` has no references. | `26` |
| **`C703`** | `SDFIRST` | _`s - ?`_ | Checks whether the first bit of _Slice_ `s` is a one. | `26` |
| **`C704`** | `SDLEXCMP` | _`s s' - x`_ | Compares the data of `s` lexicographically with the data of `s'`, returning `-1`, 0, or 1 depending on the result. | `26` |
| **`C705`** | `SDEQ` | _`s s' - ?`_ | Checks whether the data parts of `s` and `s'` coincide, equivalent to [`SDLEXCMP`](#instr-sdlexcmp) [`ISZERO`](#instr-iszero). | `26` |
| **`C708`** | `SDPFX` | _`s s' - ?`_ | Checks whether `s` is a prefix of `s'`. | `26` |
| **`C709`** | `SDPFXREV` | _`s s' - ?`_ | Checks whether `s'` is a prefix of `s`, equivalent to [`SWAP`](#instr-swap) [`SDPFX`](#instr-sdpfx). | `26` |
| **`C70A`** | `SDPPFX` | _`s s' - ?`_ | Checks whether `s` is a proper prefix of `s'` (i.e., a prefix distinct from `s'`). | `26` |
| **`C70B`** | `SDPPFXREV` | _`s s' - ?`_ | Checks whether `s'` is a proper prefix of `s`. | `26` |
| **`C70C`** | `SDSFX` | _`s s' - ?`_ | Checks whether `s` is a suffix of `s'`. | `26` |
| **`C70D`** | `SDSFXREV` | _`s s' - ?`_ | Checks whether `s'` is a suffix of `s`. | `26` |
| **`C70E`** | `SDPSFX` | _`s s' - ?`_ | Checks whether `s` is a proper suffix of `s'`. | `26` |
| **`C70F`** | `SDPSFXREV` | _`s s' - ?`_ | Checks whether `s'` is a proper suffix of `s`. | `26` |
| **`C710`** | `SDCNTLEAD0` | _`s - n`_ | Returns the number of leading zeroes in `s`. | `26` |
| **`C711`** | `SDCNTLEAD1` | _`s - n`_ | Returns the number of leading ones in `s`. | `26` |
| **`C712`** | `SDCNTTRAIL0` | _`s - n`_ | Returns the number of trailing zeroes in `s`. | `26` |
| **`C713`** | `SDCNTTRAIL1` | _`s - n`_ | Returns the number of trailing ones in `s`. | `26` |

## 7 Cell primitives
### 7.1 Cell serialization primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`C8`** | `NEWC` | _`- b`_ | Creates a new empty _Builder_. | `18` |
| **`C9`** | `ENDC` | _`b - c`_ | Converts a _Builder_ into an ordinary _Cell_. | `518` |
| **`CAcc`** | `[cc+1] STI` | _`x b - b'`_ | Stores a signed `cc+1`-bit integer `x` into _Builder_ `b` for `0 <= cc <= 255`, throws a range check exception if `x` does not fit into `cc+1` bits. | `26` |
| **`CBcc`** | `[cc+1] STU` | _`x b - b'`_ | Stores an unsigned `cc+1`-bit integer `x` into _Builder_ `b`. In all other respects it is similar to [`STI`](#instr-sti). | `26` |
| **`CC`** | `STREF` | _`c b - b'`_ | Stores a reference to _Cell_ `c` into _Builder_ `b`. | `18` |
| **`CD`** | `STBREFR`<br/>`ENDCST` | _`b b'' - b`_ | Equivalent to [`ENDC`](#instr-endc) [`SWAP`](#instr-swap) [`STREF`](#instr-stref). | `518` |
| **`CE`** | `STSLICE` | _`s b - b'`_ | Stores _Slice_ `s` into _Builder_ `b`. | `18` |
| **`CF00`** | `STIX` | _`x b l - b'`_ | Stores a signed `l`-bit integer `x` into `b` for `0 <= l <= 257`. | `26` |
| **`CF01`** | `STUX` | _`x b l - b'`_ | Stores an unsigned `l`-bit integer `x` into `b` for `0 <= l <= 256`. | `26` |
| **`CF02`** | `STIXR` | _`b x l - b'`_ | Similar to [`STIX`](#instr-stix), but with arguments in a different order. | `26` |
| **`CF03`** | `STUXR` | _`b x l - b'`_ | Similar to [`STUX`](#instr-stux), but with arguments in a different order. | `26` |
| **`CF04`** | `STIXQ` | _`x b l - x b f or b' 0`_ | A quiet version of [`STIX`](#instr-stix). If there is no space in `b`, sets `b'=b` and `f=-1`.<br/>If `x` does not fit into `l` bits, sets `b'=b` and `f=1`.<br/>If the operation succeeds, `b'` is the new _Builder_ and `f=0`.<br/>However, `0 <= l <= 257`, with a range check exception if this is not so. | `26` |
| **`CF05`** | `STUXQ` | _`x b l - x b f or b' 0`_ | A quiet version of [`STUX`](#instr-stux). | `26` |
| **`CF06`** | `STIXRQ` | _`b x l - b x f or b' 0`_ | A quiet version of [`STIXR`](#instr-stixr). | `26` |
| **`CF07`** | `STUXRQ` | _`b x l - b x f or b' 0`_ | A quiet version of [`STUXR`](#instr-stuxr). | `26` |
| **`CF08cc`** | `[cc+1] STI_l` | _`x b - b'`_ | A longer version of [`[cc+1] STI`](#instr-sti). | `34` |
| **`CF09cc`** | `[cc+1] STU_l` | _`x b - b'`_ | A longer version of [`[cc+1] STU`](#instr-stu). | `34` |
| **`CF0Acc`** | `[cc+1] STIR` | _`b x - b'`_ | Equivalent to [`SWAP`](#instr-swap) [`[cc+1] STI`](#instr-sti). | `34` |
| **`CF0Bcc`** | `[cc+1] STUR` | _`b x - b'`_ | Equivalent to [`SWAP`](#instr-swap) [`[cc+1] STU`](#instr-stu). | `34` |
| **`CF0Ccc`** | `[cc+1] STIQ` | _`x b - x b f or b' 0`_ | A quiet version of [`STI`](#instr-sti). | `34` |
| **`CF0Dcc`** | `[cc+1] STUQ` | _`x b - x b f or b' 0`_ | A quiet version of [`STU`](#instr-stu). | `34` |
| **`CF0Ecc`** | `[cc+1] STIRQ` | _`b x - b x f or b' 0`_ | A quiet version of [`STIR`](#instr-stir). | `34` |
| **`CF0Fcc`** | `[cc+1] STURQ` | _`b x - b x f or b' 0`_ | A quiet version of [`STUR`](#instr-stur). | `34` |
| **`CF10`** | `STREF_l` | _`c b - b'`_ | A longer version of [`STREF`](#instr-stref). | `26` |
| **`CF11`** | `STBREF` | _`b' b - b''`_ | Equivalent to [`SWAP`](#instr-swap) [`STBREFR`](#instr-stbrefr). | `526` |
| **`CF12`** | `STSLICE_l` | _`s b - b'`_ | A longer version of [`STSLICE`](#instr-stslice). | `26` |
| **`CF13`** | `STB` | _`b' b - b''`_ | Appends all data from _Builder_ `b'` to _Builder_ `b`. | `26` |
| **`CF14`** | `STREFR` | _`b c - b'`_ | Equivalent to [`SWAP`](#instr-swap) [`STREF`](#instr-stref). | `26` |
| **`CF15`** | `STBREFR_l` | _`b b' - b''`_ | A longer encoding of [`STBREFR`](#instr-stbrefr). | `526` |
| **`CF16`** | `STSLICER` | _`b s - b'`_ | Equivalent to [`SWAP`](#instr-swap) [`STSLICE`](#instr-stslice). | `26` |
| **`CF17`** | `STBR`<br/>`BCONCAT` | _`b b' - b''`_ | Concatenates two builders.<br/>Equivalent to [`SWAP`](#instr-swap) [`STB`](#instr-stb). | `26` |
| **`CF18`** | `STREFQ` | _`c b - c b -1 or b' 0`_ | Quiet version of [`STREF`](#instr-stref). | `26` |
| **`CF19`** | `STBREFQ` | _`b' b - b' b -1 or b'' 0`_ | Quiet version of [`STBREF`](#instr-stbref). | `526` |
| **`CF1A`** | `STSLICEQ` | _`s b - s b -1 or b' 0`_ | Quiet version of [`STSLICE`](#instr-stslice). | `26` |
| **`CF1B`** | `STBQ` | _`b' b - b' b -1 or b'' 0`_ | Quiet version of [`STB`](#instr-stb). | `26` |
| **`CF1C`** | `STREFRQ` | _`b c - b c -1 or b' 0`_ | Quiet version of [`STREFR`](#instr-strefr). | `26` |
| **`CF1D`** | `STBREFRQ` | _`b b' - b b' -1 or b'' 0`_ | Quiet version of [`STBREFR`](#instr-stbrefr). | `526` |
| **`CF1E`** | `STSLICERQ` | _`b s - b s -1 or b'' 0`_ | Quiet version of [`STSLICER`](#instr-stslicer). | `26` |
| **`CF1F`** | `STBRQ`<br/>`BCONCATQ` | _`b b' - b b' -1 or b'' 0`_ | Quiet version of [`STBR`](#instr-stbr). | `26` |
| **`CF20`** | `[ref] STREFCONST` | _`b - b’`_ | Equivalent to [`PUSHREF`](#instr-pushref) [`STREFR`](#instr-strefr). | `26` |
| **`CF21`** | `[ref] [ref] STREF2CONST` | _`b - b’`_ | Equivalent to [`STREFCONST`](#instr-strefconst) [`STREFCONST`](#instr-strefconst). | `26` |
| **`CF23`** |  | _`b x - c`_ | If `x!=0`, creates a _special_ or _exotic_ cell from _Builder_ `b`.<br/>The type of the exotic cell must be stored in the first 8 bits of `b`.<br/>If `x=0`, it is equivalent to [`ENDC`](#instr-endc). Otherwise some validity checks on the data and references of `b` are performed before creating the exotic cell. | `526` |
| **`CF28`** | `STILE4` | _`x b - b'`_ | Stores a little-endian signed 32-bit integer. | `26` |
| **`CF29`** | `STULE4` | _`x b - b'`_ | Stores a little-endian unsigned 32-bit integer. | `26` |
| **`CF2A`** | `STILE8` | _`x b - b'`_ | Stores a little-endian signed 64-bit integer. | `26` |
| **`CF2B`** | `STULE8` | _`x b - b'`_ | Stores a little-endian unsigned 64-bit integer. | `26` |
| **`CF30`** | `BDEPTH` | _`b - x`_ | Returns the depth of _Builder_ `b`. If no cell references are stored in `b`, then `x=0`; otherwise `x` is one plus the maximum of depths of cells referred to from `b`. | `26` |
| **`CF31`** | `BBITS` | _`b - x`_ | Returns the number of data bits already stored in _Builder_ `b`. | `26` |
| **`CF32`** | `BREFS` | _`b - y`_ | Returns the number of cell references already stored in `b`. | `26` |
| **`CF33`** | `BBITREFS` | _`b - x y`_ | Returns the numbers of both data bits and cell references in `b`. | `26` |
| **`CF35`** | `BREMBITS` | _`b - x'`_ | Returns the number of data bits that can still be stored in `b`. | `26` |
| **`CF36`** | `BREMREFS` | _`b - y'`_ | Returns the number of references that can still be stored in `b`. | `26` |
| **`CF37`** | `BREMBITREFS` | _`b - x' y'`_ | Returns the numbers of both data bits and references that can still be stored in `b`. | `26` |
| **`CF38cc`** | `[cc+1] BCHKBITS#` | _`b -`_ | Checks whether `cc+1` bits can be stored into `b`, where `0 <= cc <= 255`. | `34/84` |
| **`CF39`** | `BCHKBITS` | _`b x - `_ | Checks whether `x` bits can be stored into `b`, `0 <= x <= 1023`. If there is no space for `x` more bits in `b`, or if `x` is not within the range `0...1023`, throws an exception. | `26/76` |
| **`CF3A`** | `BCHKREFS` | _`b y - `_ | Checks whether `y` references can be stored into `b`, `0 <= y <= 7`. | `26/76` |
| **`CF3B`** | `BCHKBITREFS` | _`b x y - `_ | Checks whether `x` bits and `y` references can be stored into `b`, `0 <= x <= 1023`, `0 <= y <= 7`. | `26/76` |
| **`CF3Ccc`** | `[cc+1] BCHKBITSQ#` | _`b - ?`_ | Checks whether `cc+1` bits can be stored into `b`, where `0 <= cc <= 255`. | `34` |
| **`CF3D`** | `BCHKBITSQ` | _`b x - ?`_ | Checks whether `x` bits can be stored into `b`, `0 <= x <= 1023`. | `26` |
| **`CF3E`** | `BCHKREFSQ` | _`b y - ?`_ | Checks whether `y` references can be stored into `b`, `0 <= y <= 7`. | `26` |
| **`CF3F`** | `BCHKBITREFSQ` | _`b x y - ?`_ | Checks whether `x` bits and `y` references can be stored into `b`, `0 <= x <= 1023`, `0 <= y <= 7`. | `26` |
| **`CF40`** | `STZEROES` | _`b n - b'`_ | Stores `n` binary zeroes into _Builder_ `b`. | `26` |
| **`CF41`** | `STONES` | _`b n - b'`_ | Stores `n` binary ones into _Builder_ `b`. | `26` |
| **`CF42`** | `STSAME` | _`b n x - b'`_ | Stores `n` binary `x`es (`0 <= x <= 1`) into _Builder_ `b`. | `26` |
| **`CFC0_xysss`** | `[slice] STSLICECONST` | _`b - b'`_ | Stores a constant subslice `sss`.<br/>_Details:_ `sss` consists of `0 <= x <= 3` references and up to `8y+2` data bits, with `0 <= y <= 7`. Completion bit is assumed.<br/>Note that the assembler can replace [`STSLICECONST`](#instr-stsliceconst) with [`PUSHSLICE`](#instr-pushslice) [`STSLICER`](#instr-stslicer) if the slice is too big. | `24` |
| **`CF81`** | `STZERO` | _`b - b'`_ | Stores one binary zero. | `24` |
| **`CF83`** | `STONE` | _`b - b'`_ | Stores one binary one. | `24` |
### 7.2 Cell deserialization primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`D0`** | `CTOS` | _`c - s`_ | Converts a _Cell_ into a _Slice_. Notice that `c` must be either an ordinary cell, or an exotic cell which is automatically _loaded_ to yield an ordinary cell `c'`, converted into a _Slice_ afterwards. | `118/43` |
| **`D1`** | `ENDS` | _`s - `_ | Removes a _Slice_ `s` from the stack, and throws an exception if it is not empty. | `18/68` |
| **`D2cc`** | `[cc+1] LDI` | _`s - x s'`_ | Loads (i.e., parses) a signed `cc+1`-bit integer `x` from _Slice_ `s`, and returns the remainder of `s` as `s'`. | `26` |
| **`D3cc`** | `[cc+1] LDU` | _`s - x s'`_ | Loads an unsigned `cc+1`-bit integer `x` from _Slice_ `s`. | `26` |
| **`D4`** | `LDREF` | _`s - c s'`_ | Loads a cell reference `c` from `s`. | `18` |
| **`D5`** | `LDREFRTOS` | _`s - s' s''`_ | Equivalent to [`LDREF`](#instr-ldref) [`SWAP`](#instr-swap) [`CTOS`](#instr-ctos). | `118/43` |
| **`D6cc`** | `[cc+1] LDSLICE` | _`s - s'' s'`_ | Cuts the next `cc+1` bits of `s` into a separate _Slice_ `s''`. | `26` |
| **`D700`** | `LDIX` | _`s l - x s'`_ | Loads a signed `l`-bit (`0 <= l <= 257`) integer `x` from _Slice_ `s`, and returns the remainder of `s` as `s'`. | `26` |
| **`D701`** | `LDUX` | _`s l - x s'`_ | Loads an unsigned `l`-bit integer `x` from (the first `l` bits of) `s`, with `0 <= l <= 256`. | `26` |
| **`D702`** | `PLDIX` | _`s l - x`_ | Preloads a signed `l`-bit integer from _Slice_ `s`, for `0 <= l <= 257`. | `26` |
| **`D703`** | `PLDUX` | _`s l - x`_ | Preloads an unsigned `l`-bit integer from `s`, for `0 <= l <= 256`. | `26` |
| **`D704`** | `LDIXQ` | _`s l - x s' -1 or s 0`_ | Quiet version of [`LDIX`](#instr-ldix): loads a signed `l`-bit integer from `s` similarly to [`LDIX`](#instr-ldix), but returns a success flag, equal to `-1` on success or to `0` on failure (if `s` does not have `l` bits), instead of throwing a cell underflow exception. | `26` |
| **`D705`** | `LDUXQ` | _`s l - x s' -1 or s 0`_ | Quiet version of [`LDUX`](#instr-ldux). | `26` |
| **`D706`** | `PLDIXQ` | _`s l - x -1 or 0`_ | Quiet version of [`PLDIX`](#instr-pldix). | `26` |
| **`D707`** | `PLDUXQ` | _`s l - x -1 or 0`_ | Quiet version of [`PLDUX`](#instr-pldux). | `26` |
| **`D708cc`** | `[cc+1] LDI_l` | _`s - x s'`_ | A longer encoding for [`LDI`](#instr-ldi). | `34` |
| **`D709cc`** | `[cc+1] LDU_l` | _`s - x s'`_ | A longer encoding for [`LDU`](#instr-ldu). | `34` |
| **`D70Acc`** | `[cc+1] PLDI` | _`s - x`_ | Preloads a signed `cc+1`-bit integer from _Slice_ `s`. | `34` |
| **`D70Bcc`** | `[cc+1] PLDU` | _`s - x`_ | Preloads an unsigned `cc+1`-bit integer from `s`. | `34` |
| **`D70Ccc`** | `[cc+1] LDIQ` | _`s - x s' -1 or s 0`_ | A quiet version of [`LDI`](#instr-ldi). | `34` |
| **`D70Dcc`** | `[cc+1] LDUQ` | _`s - x s' -1 or s 0`_ | A quiet version of [`LDU`](#instr-ldu). | `34` |
| **`D70Ecc`** | `[cc+1] PLDIQ` | _`s - x -1 or 0`_ | A quiet version of [`PLDI`](#instr-pldi). | `34` |
| **`D70Fcc`** | `[cc+1] PLDUQ` | _`s - x -1 or 0`_ | A quiet version of [`PLDU`](#instr-pldu). | `34` |
| **`D714_c`** | `[32(c+1)] PLDUZ` | _`s - s x`_ | Preloads the first `32(c+1)` bits of _Slice_ `s` into an unsigned integer `x`, for `0 <= c <= 7`. If `s` is shorter than necessary, missing bits are assumed to be zero. This operation is intended to be used along with [`IFBITJMP`](#instr-ifbitjmp) and similar instructions. | `26` |
| **`D718`** | `LDSLICEX` | _`s l - s'' s'`_ | Loads the first `0 <= l <= 1023` bits from _Slice_ `s` into a separate _Slice_ `s''`, returning the remainder of `s` as `s'`. | `26` |
| **`D719`** | `PLDSLICEX` | _`s l - s''`_ | Returns the first `0 <= l <= 1023` bits of `s` as `s''`. | `26` |
| **`D71A`** | `LDSLICEXQ` | _`s l - s'' s' -1 or s 0`_ | A quiet version of [`LDSLICEX`](#instr-ldslicex). | `26` |
| **`D71B`** | `PLDSLICEXQ` | _`s l - s' -1 or 0`_ | A quiet version of [`LDSLICEXQ`](#instr-ldslicexq). | `26` |
| **`D71Ccc`** | `[cc+1] LDSLICE_l` | _`s - s'' s'`_ | A longer encoding for [`LDSLICE`](#instr-ldslice). | `34` |
| **`D71Dcc`** | `[cc+1] PLDSLICE` | _`s - s''`_ | Returns the first `0 < cc+1 <= 256` bits of `s` as `s''`. | `34` |
| **`D71Ecc`** | `[cc+1] LDSLICEQ` | _`s - s'' s' -1 or s 0`_ | A quiet version of [`LDSLICE`](#instr-ldslice). | `34` |
| **`D71Fcc`** | `[cc+1] PLDSLICEQ` | _`s - s'' -1 or 0`_ | A quiet version of [`PLDSLICE`](#instr-pldslice). | `34` |
| **`D720`** | `SDCUTFIRST` | _`s l - s'`_ | Returns the first `0 <= l <= 1023` bits of `s`. It is equivalent to [`PLDSLICEX`](#instr-pldslicex). | `26` |
| **`D721`** | `SDSKIPFIRST` | _`s l - s'`_ | Returns all but the first `0 <= l <= 1023` bits of `s`. It is equivalent to [`LDSLICEX`](#instr-ldslicex) [`NIP`](#instr-nip). | `26` |
| **`D722`** | `SDCUTLAST` | _`s l - s'`_ | Returns the last `0 <= l <= 1023` bits of `s`. | `26` |
| **`D723`** | `SDSKIPLAST` | _`s l - s'`_ | Returns all but the last `0 <= l <= 1023` bits of `s`. | `26` |
| **`D724`** | `SDSUBSTR` | _`s l l' - s'`_ | Returns `0 <= l' <= 1023` bits of `s` starting from offset `0 <= l <= 1023`, thus extracting a bit substring out of the data of `s`. | `26` |
| **`D726`** | `SDBEGINSX` | _`s s' - s''`_ | Checks whether `s` begins with (the data bits of) `s'`, and removes `s'` from `s` on success. On failure throws a cell deserialization exception. Primitive [`SDPFXREV`](#instr-sdpfxrev) can be considered a quiet version of [`SDBEGINSX`](#instr-sdbeginsx). | `26` |
| **`D727`** | `SDBEGINSXQ` | _`s s' - s'' -1 or s 0`_ | A quiet version of [`SDBEGINSX`](#instr-sdbeginsx). | `26` |
| **`D72A_xsss`** | `[slice] SDBEGINS` | _`s - s''`_ | Checks whether `s` begins with constant bitstring `sss` of length `8x+3` (with continuation bit assumed), where `0 <= x <= 127`, and removes `sss` from `s` on success. | `31` |
| **`D72E_xsss`** | `[slice] SDBEGINSQ` | _`s - s'' -1 or s 0`_ | A quiet version of [`SDBEGINS`](#instr-sdbegins). | `31` |
| **`D730`** | `SCUTFIRST` | _`s l r - s'`_ | Returns the first `0 <= l <= 1023` bits and first `0 <= r <= 4` references of `s`. | `26` |
| **`D731`** | `SSKIPFIRST` | _`s l r - s'`_ | Returns all but the first `l` bits of `s` and `r` references of `s`. | `26` |
| **`D732`** | `SCUTLAST` | _`s l r - s'`_ | Returns the last `0 <= l <= 1023` data bits and last `0 <= r <= 4` references of `s`. | `26` |
| **`D733`** | `SSKIPLAST` | _`s l r - s'`_ | Returns all but the last `l` bits of `s` and `r` references of `s`. | `26` |
| **`D734`** | `SUBSLICE` | _`s l r l' r' - s'`_ | Returns `0 <= l' <= 1023` bits and `0 <= r' <= 4` references from _Slice_ `s`, after skipping the first `0 <= l <= 1023` bits and first `0 <= r <= 4` references. | `26` |
| **`D736`** | `SPLIT` | _`s l r - s' s''`_ | Splits the first `0 <= l <= 1023` data bits and first `0 <= r <= 4` references from `s` into `s'`, returning the remainder of `s` as `s''`. | `26` |
| **`D737`** | `SPLITQ` | _`s l r - s' s'' -1 or s 0`_ | A quiet version of [`SPLIT`](#instr-split). | `26` |
| **`D739`** |  | _`c - s ?`_ | Transforms an ordinary or exotic cell into a _Slice_, as if it were an ordinary cell. A flag is returned indicating whether `c` is exotic. If that be the case, its type can later be deserialized from the first eight bits of `s`. |  |
| **`D73A`** |  | _`c - c'`_ | Loads an exotic cell `c` and returns an ordinary cell `c'`. If `c` is already ordinary, does nothing. If `c` cannot be loaded, throws an exception. |  |
| **`D73B`** |  | _`c - c' -1 or c 0`_ | Loads an exotic cell `c` and returns an ordinary cell `c'`. If `c` is already ordinary, does nothing. If `c` cannot be loaded, returns 0. |  |
| **`D741`** | `SCHKBITS` | _`s l - `_ | Checks whether there are at least `l` data bits in _Slice_ `s`. If this is not the case, throws a cell deserialisation (i.e., cell underflow) exception. | `26/76` |
| **`D742`** | `SCHKREFS` | _`s r - `_ | Checks whether there are at least `r` references in _Slice_ `s`. | `26/76` |
| **`D743`** | `SCHKBITREFS` | _`s l r - `_ | Checks whether there are at least `l` data bits and `r` references in _Slice_ `s`. | `26/76` |
| **`D745`** | `SCHKBITSQ` | _`s l - ?`_ | Checks whether there are at least `l` data bits in _Slice_ `s`. | `26` |
| **`D746`** | `SCHKREFSQ` | _`s r - ?`_ | Checks whether there are at least `r` references in _Slice_ `s`. | `26` |
| **`D747`** | `SCHKBITREFSQ` | _`s l r - ?`_ | Checks whether there are at least `l` data bits and `r` references in _Slice_ `s`. | `26` |
| **`D748`** | `PLDREFVAR` | _`s n - c`_ | Returns the `n`-th cell reference of _Slice_ `s` for `0 <= n <= 3`. | `26` |
| **`D749`** | `SBITS` | _`s - l`_ | Returns the number of data bits in _Slice_ `s`. | `26` |
| **`D74A`** | `SREFS` | _`s - r`_ | Returns the number of references in _Slice_ `s`. | `26` |
| **`D74B`** | `SBITREFS` | _`s - l r`_ | Returns both the number of data bits and the number of references in `s`. | `26` |
| **`D74E_n`** | `[n] PLDREFIDX` | _`s - c`_ | Returns the `n`-th cell reference of _Slice_ `s`, where `0 <= n <= 3`. | `26` |
| **`D74C`** | `PLDREF` | _`s - c`_ | Preloads the first cell reference of a _Slice_. | `26` |
| **`D750`** | `LDILE4` | _`s - x s'`_ | Loads a little-endian signed 32-bit integer. | `26` |
| **`D751`** | `LDULE4` | _`s - x s'`_ | Loads a little-endian unsigned 32-bit integer. | `26` |
| **`D752`** | `LDILE8` | _`s - x s'`_ | Loads a little-endian signed 64-bit integer. | `26` |
| **`D753`** | `LDULE8` | _`s - x s'`_ | Loads a little-endian unsigned 64-bit integer. | `26` |
| **`D754`** | `PLDILE4` | _`s - x`_ | Preloads a little-endian signed 32-bit integer. | `26` |
| **`D755`** | `PLDULE4` | _`s - x`_ | Preloads a little-endian unsigned 32-bit integer. | `26` |
| **`D756`** | `PLDILE8` | _`s - x`_ | Preloads a little-endian signed 64-bit integer. | `26` |
| **`D757`** | `PLDULE8` | _`s - x`_ | Preloads a little-endian unsigned 64-bit integer. | `26` |
| **`D758`** | `LDILE4Q` | _`s - x s' -1 or s 0`_ | Quietly loads a little-endian signed 32-bit integer. | `26` |
| **`D759`** | `LDULE4Q` | _`s - x s' -1 or s 0`_ | Quietly loads a little-endian unsigned 32-bit integer. | `26` |
| **`D75A`** | `LDILE8Q` | _`s - x s' -1 or s 0`_ | Quietly loads a little-endian signed 64-bit integer. | `26` |
| **`D75B`** | `LDULE8Q` | _`s - x s' -1 or s 0`_ | Quietly loads a little-endian unsigned 64-bit integer. | `26` |
| **`D75C`** | `PLDILE4Q` | _`s - x -1 or 0`_ | Quietly preloads a little-endian signed 32-bit integer. | `26` |
| **`D75D`** | `PLDULE4Q` | _`s - x -1 or 0`_ | Quietly preloads a little-endian unsigned 32-bit integer. | `26` |
| **`D75E`** | `PLDILE8Q` | _`s - x -1 or 0`_ | Quietly preloads a little-endian signed 64-bit integer. | `26` |
| **`D75F`** | `PLDULE8Q` | _`s - x -1 or 0`_ | Quietly preloads a little-endian unsigned 64-bit integer. | `26` |
| **`D760`** | `LDZEROES` | _`s - n s'`_ | Returns the count `n` of leading zero bits in `s`, and removes these bits from `s`. | `26` |
| **`D761`** | `LDONES` | _`s - n s'`_ | Returns the count `n` of leading one bits in `s`, and removes these bits from `s`. | `26` |
| **`D762`** | `LDSAME` | _`s x - n s'`_ | Returns the count `n` of leading bits equal to `0 <= x <= 1` in `s`, and removes these bits from `s`. | `26` |
| **`D764`** | `SDEPTH` | _`s - x`_ | Returns the depth of _Slice_ `s`. If `s` has no references, then `x=0`; otherwise `x` is one plus the maximum of depths of cells referred to from `s`. | `26` |
| **`D765`** | `CDEPTH` | _`c - x`_ | Returns the depth of _Cell_ `c`. If `c` has no references, then `x=0`; otherwise `x` is one plus the maximum of depths of cells referred to from `c`. If `c` is a _Null_ instead of a _Cell_, returns zero. | `26` |

## 8 Continuation and control flow primitives
### 8.1 Unconditional control flow primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`D8`** | `EXECUTE`<br/>`CALLX` | _`c - `_ | _Calls_, or _executes_, continuation `c`. | `18` |
| **`D9`** | `JMPX` | _`c - `_ | _Jumps_, or transfers control, to continuation `c`.<br/>The remainder of the previous current continuation `cc` is discarded. | `18` |
| **`DApr`** | `[p] [r] CALLXARGS` | _`c - `_ | _Calls_ continuation `c` with `p` parameters and expecting `r` return values<br/>`0 <= p <= 15`, `0 <= r <= 15` | `26` |
| **`DB0p`** | `[p] -1 CALLXARGS` | _`c - `_ | _Calls_ continuation `c` with `0 <= p <= 15` parameters, expecting an arbitrary number of return values. | `26` |
| **`DB1p`** | `[p] JMPXARGS` | _`c - `_ | _Jumps_ to continuation `c`, passing only the top `0 <= p <= 15` values from the current stack to it (the remainder of the current stack is discarded). | `26` |
| **`DB2r`** | `[r] RETARGS` |  | _Returns_ to `c0`, with `0 <= r <= 15` return values taken from the current stack. | `26` |
| **`DB30`** | `RET`<br/>`RETTRUE` |  | _Returns_ to the continuation at `c0`. The remainder of the current continuation `cc` is discarded.<br/>Approximately equivalent to [`c0 PUSHCTR`](#instr-pushctr) [`JMPX`](#instr-jmpx). | `26` |
| **`DB31`** | `RETALT`<br/>`RETFALSE` |  | _Returns_ to the continuation at `c1`.<br/>Approximately equivalent to [`c1 PUSHCTR`](#instr-pushctr) [`JMPX`](#instr-jmpx). | `26` |
| **`DB32`** | `BRANCH`<br/>`RETBOOL` | _`f - `_ | Performs [`RETTRUE`](#instr-ret) if integer `f!=0`, or [`RETFALSE`](#instr-retalt) if `f=0`. | `26` |
| **`DB34`** | `CALLCC` | _`c - `_ | _Call with current continuation_, transfers control to `c`, pushing the old value of `cc` into `c`'s stack (instead of discarding it or writing it into new `c0`). | `26` |
| **`DB35`** | `JMPXDATA` | _`c - `_ | Similar to [`CALLCC`](#instr-callcc), but the remainder of the current continuation (the old value of `cc`) is converted into a _Slice_ before pushing it into the stack of `c`. | `26` |
| **`DB36pr`** | `[p] [r] CALLCCARGS` | _`c - `_ | Similar to [`CALLXARGS`](#instr-callxargs), but pushes the old value of `cc` (along with the top `0 <= p <= 15` values from the original stack) into the stack of newly-invoked continuation `c`, setting `cc.nargs` to `-1 <= r <= 14`. | `34` |
| **`DB38`** | `CALLXVARARGS` | _`c p r - `_ | Similar to [`CALLXARGS`](#instr-callxargs), but takes `-1 <= p,r <= 254` from the stack. The next three operations also take `p` and `r` from the stack, both in the range `-1...254`. | `26` |
| **`DB39`** | `RETVARARGS` | _`p r - `_ | Similar to [`RETARGS`](#instr-retargs). | `26` |
| **`DB3A`** | `JMPXVARARGS` | _`c p r - `_ | Similar to [`JMPXARGS`](#instr-jmpxargs). | `26` |
| **`DB3B`** | `CALLCCVARARGS` | _`c p r - `_ | Similar to [`CALLCCARGS`](#instr-callccargs). | `26` |
| **`DB3C`** | `[ref] CALLREF` |  | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`CALLX`](#instr-execute). | `126/51` |
| **`DB3D`** | `[ref] JMPREF` |  | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`JMPX`](#instr-jmpx). | `126/51` |
| **`DB3E`** | `[ref] JMPREFDATA` |  | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`JMPXDATA`](#instr-jmpxdata). | `126/51` |
| **`DB3F`** | `RETDATA` |  | Equivalent to [`c0 PUSHCTR`](#instr-pushctr) [`JMPXDATA`](#instr-jmpxdata). In this way, the remainder of the current continuation is converted into a _Slice_ and returned to the caller. | `26` |
### 8.2 Conditional control flow primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`DC`** | `IFRET`<br/>`IFNOT:` | _`f - `_ | Performs a [`RET`](#instr-ret), but only if integer `f` is non-zero. If `f` is a `NaN`, throws an integer overflow exception. | `18` |
| **`DD`** | `IFNOTRET`<br/>`IF:` | _`f - `_ | Performs a [`RET`](#instr-ret), but only if integer `f` is zero. | `18` |
| **`DE`** | `IF` | _`f c - `_ | Performs [`EXECUTE`](#instr-execute) for `c` (i.e., _executes_ `c`), but only if integer `f` is non-zero. Otherwise simply discards both values. | `18` |
| **`DE`** | `IF:<{ code }>`<br/>`<{ code }>IF` | _`f -`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`IF`](#instr-if). |  |
| **`DF`** | `IFNOT` | _`f c - `_ | Executes continuation `c`, but only if integer `f` is zero. Otherwise simply discards both values. | `18` |
| **`DF`** | `IFNOT:<{ code }>`<br/>`<{ code }>IFNOT` | _`f -`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`IFNOT`](#instr-ifnot). |  |
| **`E0`** | `IFJMP` | _`f c - `_ | Jumps to `c` (similarly to [`JMPX`](#instr-jmpx)), but only if `f` is non-zero. | `18` |
| **`E0`** | `IFJMP:<{ code }>` | _`f -`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`IFJMP`](#instr-ifjmp). |  |
| **`E1`** | `IFNOTJMP` | _`f c - `_ | Jumps to `c` (similarly to [`JMPX`](#instr-jmpx)), but only if `f` is zero. | `18` |
| **`E1`** | `IFNOTJMP:<{ code }>` | _`f -`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`IFNOTJMP`](#instr-ifnotjmp). |  |
| **`E2`** | `IFELSE` | _`f c c' - `_ | If integer `f` is non-zero, executes `c`, otherwise executes `c'`. Equivalent to [`CONDSELCHK`](#instr-condselchk) [`EXECUTE`](#instr-execute). | `18` |
| **`E2`** | `IF:<{ code1 }>ELSE<{ code2 }>` | _`f -`_ | Equivalent to [`<{ code1 }> CONT`](#instr-pushcont) [`<{ code2 }> CONT`](#instr-pushcont) [`IFELSE`](#instr-ifelse). |  |
| **`E300`** | `[ref] IFREF` | _`f - `_ | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`IF`](#instr-if), with the optimization that the cell reference is not actually loaded into a _Slice_ and then converted into an ordinary _Continuation_ if `f=0`.<br/>Gas consumption of this primitive depends on whether `f=0` and whether the reference was loaded before.<br/>Similar remarks apply other primitives that accept a continuation as a reference. | `26/126/51` |
| **`E301`** | `[ref] IFNOTREF` | _`f - `_ | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`IFNOT`](#instr-ifnot). | `26/126/51` |
| **`E302`** | `[ref] IFJMPREF` | _`f - `_ | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`IFJMP`](#instr-ifjmp). | `26/126/51` |
| **`E303`** | `[ref] IFNOTJMPREF` | _`f - `_ | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`IFNOTJMP`](#instr-ifnotjmp). | `26/126/51` |
| **`E304`** | `CONDSEL` | _`f x y - x or y`_ | If integer `f` is non-zero, returns `x`, otherwise returns `y`. Notice that no type checks are performed on `x` and `y`; as such, it is more like a conditional stack operation. Roughly equivalent to [`ROT`](#instr-rot) [`ISZERO`](#instr-iszero) [`INC`](#instr-inc) [`ROLLX`](#instr-rollx) [`NIP`](#instr-nip). | `26` |
| **`E305`** | `CONDSELCHK` | _`f x y - x or y`_ | Same as [`CONDSEL`](#instr-condsel), but first checks whether `x` and `y` have the same type. | `26` |
| **`E308`** | `IFRETALT` | _`f -`_ | Performs [`RETALT`](#instr-retalt) if integer `f!=0`. | `26` |
| **`E309`** | `IFNOTRETALT` | _`f -`_ | Performs [`RETALT`](#instr-retalt) if integer `f=0`. | `26` |
| **`E30D`** | `[ref] IFREFELSE` | _`f c -`_ | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`SWAP`](#instr-swap) [`IFELSE`](#instr-ifelse), with the optimization that the cell reference is not actually loaded into a _Slice_ and then converted into an ordinary _Continuation_ if `f=0`. Similar remarks apply to the next two primitives: cells are converted into continuations only when necessary. | `26/126/51` |
| **`E30E`** | `[ref] IFELSEREF` | _`f c -`_ | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`IFELSE`](#instr-ifelse). | `26/126/51` |
| **`E30F`** | `[ref] [ref] IFREFELSEREF` | _`f -`_ | Equivalent to [`PUSHREFCONT`](#instr-pushrefcont) [`PUSHREFCONT`](#instr-pushrefcont) [`IFELSE`](#instr-ifelse). | `126/51` |
| **`E39_n`** | `[n] IFBITJMP` | _`x c - x`_ | Checks whether bit `0 <= n <= 31` is set in integer `x`, and if so, performs [`JMPX`](#instr-jmpx) to continuation `c`. Value `x` is left in the stack. | `26` |
| **`E3B_n`** | `[n] IFNBITJMP` | _`x c - x`_ | Jumps to `c` if bit `0 <= n <= 31` is not set in integer `x`. | `26` |
| **`E3D_n`** | `[ref] [n] IFBITJMPREF` | _`x - x`_ | Performs a [`JMPREF`](#instr-jmpref) if bit `0 <= n <= 31` is set in integer `x`. | `126/51` |
| **`E3F_n`** | `[ref] [n] IFNBITJMPREF` | _`x - x`_ | Performs a [`JMPREF`](#instr-jmpref) if bit `0 <= n <= 31` is not set in integer `x`. | `126/51` |
### 8.3 Control flow primitives: loops
| xxxxxxx<br />Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`E4`** | `REPEAT` | _`n c - `_ | Executes continuation `c` `n` times, if integer `n` is non-negative. If `n>=2^31` or `n<-2^31`, generates a range check exception.<br/>Notice that a [`RET`](#instr-ret) inside the code of `c` works as a `continue`, not as a `break`. One should use either alternative (experimental) loops or alternative [`RETALT`](#instr-retalt) (along with a [`SETEXITALT`](#instr-setexitalt) before the loop) to `break` out of a loop. | `18` |
| **`E4`** | `REPEAT:<{ code }>`<br/>`<{ code }>REPEAT` | _`n -`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`REPEAT`](#instr-repeat). |  |
| **`E5`** | `REPEATEND`<br/>`REPEAT:` | _`n - `_ | Similar to [`REPEAT`](#instr-repeat), but it is applied to the current continuation `cc`. | `18` |
| **`E6`** | `UNTIL` | _`c - `_ | Executes continuation `c`, then pops an integer `x` from the resulting stack. If `x` is zero, performs another iteration of this loop. The actual implementation of this primitive involves an extraordinary continuation `ec_until` with its arguments set to the body of the loop (continuation `c`) and the original current continuation `cc`. This extraordinary continuation is then saved into the savelist of `c` as `c.c0` and the modified `c` is then executed. The other loop primitives are implemented similarly with the aid of suitable extraordinary continuations. | `18` |
| **`E6`** | `UNTIL:<{ code }>`<br/>`<{ code }>UNTIL` | _`-`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`UNTIL`](#instr-until). |  |
| **`E7`** | `UNTILEND`<br/>`UNTIL:` | _`-`_ | Similar to [`UNTIL`](#instr-until), but executes the current continuation `cc` in a loop. When the loop exit condition is satisfied, performs a [`RET`](#instr-ret). | `18` |
| **`E8`** | `WHILE` | _`c' c - `_ | Executes `c'` and pops an integer `x` from the resulting stack. If `x` is zero, exists the loop and transfers control to the original `cc`. If `x` is non-zero, executes `c`, and then begins a new iteration. | `18` |
| **`E8`** | `WHILE:<{ cond }>DO<{ code }>` | _`-`_ | Equivalent to [`<{ cond }> CONT`](#instr-pushcont) [`<{ code }> CONT`](#instr-pushcont) [`WHILE`](#instr-while). |  |
| **`E9`** | `WHILEEND` | _`c' - `_ | Similar to [`WHILE`](#instr-while), but uses the current continuation `cc` as the loop body. | `18` |
| **`EA`** | `AGAIN` | _`c - `_ | Similar to [`REPEAT`](#instr-repeat), but executes `c` infinitely many times. A [`RET`](#instr-ret) only begins a new iteration of the infinite loop, which can be exited only by an exception, or a [`RETALT`](#instr-retalt) (or an explicit [`JMPX`](#instr-jmpx)). | `18` |
| **`EA`** | `AGAIN:<{ code }>`<br/>`<{ code }>AGAIN` | _`-`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`AGAIN`](#instr-again). |  |
| **`EB`** | `AGAINEND`<br/>`AGAIN:` | _`-`_ | Similar to [`AGAIN`](#instr-again), but performed with respect to the current continuation `cc`. | `18` |
| **`E314`** | `REPEATBRK` | _`n c -`_ | Similar to [`REPEAT`](#instr-repeat), but also sets `c1` to the original `cc` after saving the old value of `c1` into the savelist of the original `cc`. In this way [`RETALT`](#instr-retalt) could be used to break out of the loop body. | `26` |
| **`E314`** | `REPEATBRK:<{ code }>`<br/>`<{ code }>REPEATBRK` | _`n -`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`REPEATBRK`](#instr-repeatbrk). |  |
| **`E315`** | `REPEATENDBRK` | _`n -`_ | Similar to [`REPEATEND`](#instr-repeatend), but also sets `c1` to the original `c0` after saving the old value of `c1` into the savelist of the original `c0`. Equivalent to [`SAMEALTSAVE`](#instr-samealtsave) [`REPEATEND`](#instr-repeatend). | `26` |
| **`E316`** | `UNTILBRK` | _`c -`_ | Similar to [`UNTIL`](#instr-until), but also modifies `c1` in the same way as [`REPEATBRK`](#instr-repeatbrk). | `26` |
| **`E316`** | `UNTILBRK:<{ code }>` | _`-`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`UNTILBRK`](#instr-untilbrk). |  |
| **`E317`** | `UNTILENDBRK`<br/>`UNTILBRK:` | _`-`_ | Equivalent to [`SAMEALTSAVE`](#instr-samealtsave) [`UNTILEND`](#instr-untilend). | `26` |
| **`E318`** | `WHILEBRK` | _`c' c -`_ | Similar to [`WHILE`](#instr-while), but also modifies `c1` in the same way as [`REPEATBRK`](#instr-repeatbrk). | `26` |
| **`E318`** | `WHILEBRK:<{ cond }>DO<{ code }>` | _`-`_ | Equivalent to [`<{ cond }> CONT`](#instr-pushcont) [`<{ code }> CONT`](#instr-pushcont) [`WHILEBRK`](#instr-whilebrk). |  |
| **`E319`** | `WHILEENDBRK` | _`c -`_ | Equivalent to [`SAMEALTSAVE`](#instr-samealtsave) [`WHILEEND`](#instr-whileend). | `26` |
| **`E31A`** | `AGAINBRK` | _`c -`_ | Similar to [`AGAIN`](#instr-again), but also modifies `c1` in the same way as [`REPEATBRK`](#instr-repeatbrk). | `26` |
| **`E31A`** | `AGAINBRK:<{ code }>` | _`-`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`AGAINBRK`](#instr-againbrk). |  |
| **`E31B`** | `AGAINENDBRK`<br/>`AGAINBRK:` | _`-`_ | Equivalent to [`SAMEALTSAVE`](#instr-samealtsave) [`AGAINEND`](#instr-againend). | `26` |
### 8.4 Manipulating the stack of continuations
Here `s"` is the [fee for moving stack elements between continuations](#11-gas-prices). It is equal to the size of the resulting stack minus 32 (or 0 if the stack is smaller than 32).

| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`ECrn`** | `[r] [n] SETCONTARGS` | _`x_1 x_2...x_r c - c'`_ | Similar to [`[r] -1 SETCONTARGS`](#instr-setcontargs-n), but sets `c.nargs` to the final size of the stack of `c'` plus `n`. In other words, transforms `c` into a _closure_ or a _partially applied function_, with `0 <= n <= 14` arguments missing. | `26+s”` |
| **`EC0n`** | `[n] SETNUMARGS` | _`c - c'`_ | Sets `c.nargs` to `n` plus the current depth of `c`'s stack, where `0 <= n <= 14`. If `c.nargs` is already set to a non-negative value, does nothing. | `26` |
| **`ECrF`** | `[r] -1 SETCONTARGS` | _`x_1 x_2...x_r c - c'`_ | Pushes `0 <= r <= 15` values `x_1...x_r` into the stack of (a copy of) the continuation `c`, starting with `x_1`. If the final depth of `c`'s stack turns out to be greater than `c.nargs`, a stack overflow exception is generated. | `26+s”` |
| **`ED0p`** | `[p] RETURNARGS` | _`-`_ | Leaves only the top `0 <= p <= 15` values in the current stack (somewhat similarly to [`ONLYTOPX`](#instr-onlytopx)), with all the unused bottom values not discarded, but saved into continuation `c0` in the same way as [`SETCONTARGS`](#instr-setcontargs-n) does. | `26+s”` |
| **`ED10`** | `RETURNVARARGS` | _`p -`_ | Similar to [`RETURNARGS`](#instr-returnargs), but with Integer `0 <= p <= 255` taken from the stack. | `26+s”` |
| **`ED11`** | `SETCONTVARARGS` | _`x_1 x_2...x_r c r n - c'`_ | Similar to [`SETCONTARGS`](#instr-setcontargs-n), but with `0 <= r <= 255` and `-1 <= n <= 255` taken from the stack. | `26+s”` |
| **`ED12`** | `SETNUMVARARGS` | _`c n - c'`_ | `-1 <= n <= 255`<br/>If `n=-1`, this operation does nothing (`c'=c`).<br/>Otherwise its action is similar to [`[n] SETNUMARGS`](#instr-setnumargs), but with `n` taken from the stack. | `26` |
### 8.5 Creating simple continuations and closures
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`ED1E`** | `BLESS` | _`s - c`_ | Transforms a _Slice_ `s` into a simple ordinary continuation `c`, with `c.code=s` and an empty stack and savelist. | `26` |
| **`ED1F`** | `BLESSVARARGS` | _`x_1...x_r s r n - c`_ | Equivalent to [`ROT`](#instr-rot) [`BLESS`](#instr-bless) [`ROTREV`](#instr-rotrev) [`SETCONTVARARGS`](#instr-setcontvarargs). | `26+s”` |
| **`EErn`** | `[r] [n] BLESSARGS` | _`x_1...x_r s - c`_ | `0 <= r <= 15`, `-1 <= n <= 14`<br/>Equivalent to [`BLESS`](#instr-bless) [`[r] [n] SETCONTARGS`](#instr-setcontargs-n).<br/>The value of `n` is represented inside the instruction by the 4-bit integer `n mod 16`. | `26` |
| **`EE0n`** | `[n] BLESSNUMARGS` | _`s - c`_ | Also transforms a _Slice_ `s` into a _Continuation_ `c`, but sets `c.nargs` to `0 <= n <= 14`. | `26` |
### 8.6 Operations with continuation savelists and control registers
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`ED4i`** | `c[i] PUSHCTR`<br/>`c[i] PUSH` | _`- x`_ | Pushes the current value of control register `c(i)`. If the control register is not supported in the current codepage, or if it does not have a value, an exception is triggered. | `26` |
| **`ED44`** | `c4 PUSHCTR`<br/>`c4 PUSH` | _`- x`_ | Pushes the “global data root'' cell reference, thus enabling access to persistent smart-contract data. | `26` |
| **`ED5i`** | `c[i] POPCTR`<br/>`c[i] POP` | _`x - `_ | Pops a value `x` from the stack and stores it into control register `c(i)`, if supported in the current codepage. Notice that if a control register accepts only values of a specific type, a type-checking exception may occur. | `26` |
| **`ED54`** | `c4 POPCTR`<br/>`c4 POP` | _`x -`_ | Sets the “global data root'' cell reference, thus allowing modification of persistent smart-contract data. | `26` |
| **`ED6i`** | `c[i] SETCONT`<br/>`c[i] SETCONTCTR` | _`x c - c'`_ | Stores `x` into the savelist of continuation `c` as `c(i)`, and returns the resulting continuation `c'`. Almost all operations with continuations may be expressed in terms of [`SETCONTCTR`](#instr-setcontctr), [`POPCTR`](#instr-popctr), and [`PUSHCTR`](#instr-pushctr). | `26` |
| **`ED7i`** | `c[i] SETRETCTR` | _`x - `_ | Equivalent to [`c0 PUSHCTR`](#instr-pushctr) [`c[i] SETCONTCTR`](#instr-setcontctr) [`c0 POPCTR`](#instr-popctr). | `26` |
| **`ED8i`** | `c[i] SETALTCTR` | _`x - `_ | Equivalent to [`c1 PUSHCTR`](#instr-pushctr) [`c[i] SETCONTCTR`](#instr-setcontctr) [`c0 POPCTR`](#instr-popctr). | `26` |
| **`ED9i`** | `c[i] POPSAVE`<br/>`c[i] POPCTRSAVE` | _`x -`_ | Similar to [`c[i] POPCTR`](#instr-popctr), but also saves the old value of `c[i]` into continuation `c0`.<br/>Equivalent (up to exceptions) to [`c[i] SAVECTR`](#instr-save) [`c[i] POPCTR`](#instr-popctr). | `26` |
| **`EDAi`** | `c[i] SAVE`<br/>`c[i] SAVECTR` |  | Saves the current value of `c(i)` into the savelist of continuation `c0`. If an entry for `c[i]` is already present in the savelist of `c0`, nothing is done. Equivalent to [`c[i] PUSHCTR`](#instr-pushctr) [`c[i] SETRETCTR`](#instr-setretctr). | `26` |
| **`EDBi`** | `c[i] SAVEALT`<br/>`c[i] SAVEALTCTR` |  | Similar to [`c[i] SAVE`](#instr-save), but saves the current value of `c[i]` into the savelist of `c1`, not `c0`. | `26` |
| **`EDCi`** | `c[i] SAVEBOTH`<br/>`c[i] SAVEBOTHCTR` |  | Equivalent to [`DUP`](#instr-dup) [`c[i] SAVE`](#instr-save) [`c[i] SAVEALT`](#instr-savealt). | `26` |
| **`EDE0`** | `PUSHCTRX` | _`i - x`_ | Similar to [`c[i] PUSHCTR`](#instr-pushctr), but with `i`, `0 <= i <= 255`, taken from the stack.<br/>Notice that this primitive is one of the few “exotic'' primitives, which are not polymorphic like stack manipulation primitives, and at the same time do not have well-defined types of parameters and return values, because the type of `x` depends on `i`. | `26` |
| **`EDE1`** | `POPCTRX` | _`x i - `_ | Similar to [`c[i] POPCTR`](#instr-popctr), but with `0 <= i <= 255` from the stack. | `26` |
| **`EDE2`** | `SETCONTCTRX` | _`x c i - c'`_ | Similar to [`c[i] SETCONTCTR`](#instr-setcontctr), but with `0 <= i <= 255` from the stack. | `26` |
| **`EDF0`** | `COMPOS`<br/>`BOOLAND` | _`c c' - c''`_ | Computes the composition `compose0(c, c’)`, which has the meaning of “perform `c`, and, if successful, perform `c'`'' (if `c` is a boolean circuit) or simply “perform `c`, then `c'`''. Equivalent to [`SWAP`](#instr-swap) [`c0 SETCONT`](#instr-setcontctr). | `26` |
| **`EDF1`** | `COMPOSALT`<br/>`BOOLOR` | _`c c' - c''`_ | Computes the alternative composition `compose1(c, c’)`, which has the meaning of “perform `c`, and, if not successful, perform `c'`'' (if `c` is a boolean circuit). Equivalent to [`SWAP`](#instr-swap) [`c1 SETCONT`](#instr-setcontctr). | `26` |
| **`EDF2`** | `COMPOSBOTH` | _`c c' - c''`_ | Computes composition `compose1(compose0(c, c’), c’)`, which has the meaning of “compute boolean circuit `c`, then compute `c'`, regardless of the result of `c`''. | `26` |
| **`EDF3`** | `ATEXIT` | _`c - `_ | Sets `c0` to `compose0(c, c0)`. In other words, `c` will be executed before exiting current subroutine. | `26` |
| **`EDF3`** | `ATEXIT:<{ code }>`<br/>`<{ code }>ATEXIT` | _`-`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`ATEXIT`](#instr-atexit). |  |
| **`EDF4`** | `ATEXITALT` | _`c - `_ | Sets `c1` to `compose1(c, c1)`. In other words, `c` will be executed before exiting current subroutine by its alternative return path. | `26` |
| **`EDF4`** | `ATEXITALT:<{ code }>`<br/>`<{ code }>ATEXITALT` | _`-`_ | Equivalent to [`<{ code }> CONT`](#instr-pushcont) [`ATEXITALT`](#instr-atexitalt). |  |
| **`EDF5`** | `SETEXITALT` | _`c - `_ | Sets `c1` to `compose1(compose0(c, c0), c1)`,<br/>In this way, a subsequent [`RETALT`](#instr-retalt) will first execute `c`, then transfer control to the original `c0`. This can be used, for instance, to exit from nested loops. | `26` |
| **`EDF6`** | `THENRET` | _`c - c'`_ | Computes `compose0(c, c0)`. | `26` |
| **`EDF7`** | `THENRETALT` | _`c - c'`_ | Computes `compose0(c, c1)` | `26` |
| **`EDF8`** | `INVERT` | _`-`_ | Interchanges `c0` and `c1`. | `26` |
| **`EDF9`** | `BOOLEVAL` | _`c - ?`_ | Performs `cc:=compose1(compose0(c, compose0(-1 PUSHINT, cc)), compose0(0 PUSHINT, cc))`. If `c` represents a boolean circuit, the net effect is to evaluate it and push either `-1` or `0` into the stack before continuing. | `26` |
| **`EDFA`** | `SAMEALT` | _`-`_ | Sets `c1` to `c0`. Equivalent to [`c0 PUSHCTR`](#instr-pushctr) [`c1 POPCTR`](#instr-popctr). | `26` |
| **`EDFB`** | `SAMEALTSAVE` | _`-`_ | Sets `c1` to `c0`, but first saves the old value of `c1` into the savelist of `c0`.<br/>Equivalent to [`c1 SAVE`](#instr-save) [`SAMEALT`](#instr-samealt). | `26` |
### 8.7 Dictionary subroutine calls and jumps
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F0nn`** | `[nn] CALL`<br/>`[nn] CALLDICT` | _`- nn`_ | Calls the continuation in `c3`, pushing integer `0 <= nn <= 255` into its stack as an argument.<br/>Approximately equivalent to [`[nn] PUSHINT`](#instr-pushint-4) [`c3 PUSHCTR`](#instr-pushctr) [`EXECUTE`](#instr-execute). |  |
| **`F12_n`** | `[n] CALL`<br/>`[n] CALLDICT` | _`- n`_ | For `0 <= n < 2^14`, an encoding of [`[n] CALL`](#instr-calldict) for larger values of `n`. |  |
| **`F16_n`** | `[n] JMP` | _` - n`_ | Jumps to the continuation in `c3`, pushing integer `0 <= n < 2^14` as its argument.<br/>Approximately equivalent to [`n PUSHINT`](#instr-pushint-4) [`c3 PUSHCTR`](#instr-pushctr) [`JMPX`](#instr-jmpx). |  |
| **`F1A_n`** | `[n] PREPARE`<br/>`[n] PREPAREDICT` | _` - n c`_ | Equivalent to [`n PUSHINT`](#instr-pushint-4) [`c3 PUSHCTR`](#instr-pushctr), for `0 <= n < 2^14`.<br/>In this way, [`[n] CALL`](#instr-calldict) is approximately equivalent to [`[n] PREPARE`](#instr-preparedict) [`EXECUTE`](#instr-execute), and [`[n] JMP`](#instr-jmpdict) is approximately equivalent to [`[n] PREPARE`](#instr-preparedict) [`JMPX`](#instr-jmpx).<br/>One might use, for instance, [`CALLXARGS`](#instr-callxargs) or [`CALLCC`](#instr-callcc) instead of [`EXECUTE`](#instr-execute) here. |  |

## 9 Exception generating and handling primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F22_n`** | `[n] THROW` | _` - 0 n`_ | Throws exception `0 <= n <= 63` with parameter zero.<br/>In other words, it transfers control to the continuation in `c2`, pushing `0` and `n` into its stack, and discarding the old stack altogether. | `76` |
| **`F26_n`** | `[n] THROWIF` | _`f - `_ | Throws exception `0 <= n <= 63` with  parameter zero only if integer `f!=0`. | `26/76` |
| **`F2A_n`** | `[n] THROWIFNOT` | _`f - `_ | Throws exception `0 <= n <= 63` with parameter zero only if integer `f=0`. | `26/76` |
| **`F2C4_n`** | `[n] THROW` | _`- 0 nn`_ | For `0 <= n < 2^11`, an encoding of [`[n] THROW`](#instr-throw-short) for larger values of `n`. | `84` |
| **`F2CC_n`** | `[n] THROWARG` | _`x - x nn`_ | Throws exception `0 <= n <  2^11` with parameter `x`, by copying `x` and `n` into the stack of `c2` and transferring control to `c2`. | `84` |
| **`F2D4_n`** | `[n] THROWIF` | _`f - `_ | For `0 <= n < 2^11`, an encoding of [`[n] THROWIF`](#instr-throwif-short) for larger values of `n`. | `34/84` |
| **`F2DC_n`** | `[n] THROWARGIF` | _`x f - `_ | Throws exception `0 <= nn < 2^11` with parameter `x` only if integer `f!=0`. | `34/84` |
| **`F2E4_n`** | `[n] THROWIFNOT` | _`f - `_ | For `0 <= n < 2^11`, an encoding of [`[n] THROWIFNOT`](#instr-throwifnot-short) for larger values of `n`. | `34/84` |
| **`F2EC_n`** | `[n] THROWARGIFNOT` | _`x f - `_ | Throws exception `0 <= n < 2^11` with parameter `x` only if integer `f=0`. | `34/84` |
| **`F2F0`** | `THROWANY` | _`n - 0 n`_ | Throws exception `0 <= n < 2^16` with parameter zero.<br/>Approximately equivalent to [`ZERO`](#instr-zero) [`SWAP`](#instr-swap) [`THROWARGANY`](#instr-throwargany). | `76` |
| **`F2F1`** | `THROWARGANY` | _`x n - x n`_ | Throws exception `0 <= n < 2^16` with parameter `x`, transferring control to the continuation in `c2`.<br/>Approximately equivalent to [`c2 PUSHCTR`](#instr-pushctr) [`2 JMPXARGS`](#instr-jmpxargs). | `76` |
| **`F2F2`** | `THROWANYIF` | _`n f - `_ | Throws exception `0 <= n < 2^16` with parameter zero only if `f!=0`. | `26/76` |
| **`F2F3`** | `THROWARGANYIF` | _`x n f - `_ | Throws exception `0 <= n<2^16` with parameter `x` only if `f!=0`. | `26/76` |
| **`F2F4`** | `THROWANYIFNOT` | _`n f - `_ | Throws exception `0 <= n<2^16` with parameter zero only if `f=0`. | `26/76` |
| **`F2F5`** | `THROWARGANYIFNOT` | _`x n f - `_ | Throws exception `0 <= n<2^16` with parameter `x` only if `f=0`. | `26/76` |
| **`F2FF`** | `TRY` | _`c c' - `_ | Sets `c2` to `c'`, first saving the old value of `c2` both into the savelist of `c'` and into the savelist of the current continuation, which is stored into `c.c0` and `c'.c0`. Then runs `c` similarly to [`EXECUTE`](#instr-execute). If `c` does not throw any exceptions, the original value of `c2` is automatically restored on return from `c`. If an exception occurs, the execution is transferred to `c'`, but the original value of `c2` is restored in the process, so that `c'` can re-throw the exception by [`THROWANY`](#instr-throwany) if it cannot handle it by itself. | `26` |
| **`F2FF`** | `TRY:<{ code1 }>CATCH<{ code2 }>` | _`-`_ | Equivalent to [`<{ code1 }> CONT`](#instr-pushcont) [`<{ code2 }> CONT`](#instr-pushcont) [`TRY`](#instr-try). |  |
| **`F3pr`** | `[p] [r] TRYARGS` | _`c c' - `_ | Similar to [`TRY`](#instr-try), but with [`[p] [r] CALLXARGS`](#instr-callxargs) internally used instead of [`EXECUTE`](#instr-execute).<br/>In this way, all but the top `0 <= p <= 15` stack elements will be saved into current continuation's stack, and then restored upon return from either `c` or `c'`, with the top `0 <= r <= 15` values of the resulting stack of `c` or `c'` copied as return values. | `26` |

## 10 Dictionary manipulation primitives
The gas consumption of most dictionary operations is not fixed, it depends on the contents of the given dictionary.
### 10.1 Dictionary creation
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`6D`** | `NEWDICT` | _` - D`_ | Returns a new empty dictionary.<br/>It is an alternative mnemonics for [`PUSHNULL`](#instr-null). | `18` |
| **`6E`** | `DICTEMPTY` | _`D - ?`_ | Checks whether dictionary `D` is empty, and returns `-1` or `0` accordingly.<br/>It is an alternative mnemonics for [`ISNULL`](#instr-isnull). | `18` |
### 10.2 Dictionary serialization and deserialization
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`CE`** | `STDICTS`<br/>`` | _`s b - b'`_ | Stores a _Slice_-represented dictionary `s` into _Builder_ `b`.<br/>It is actually a synonym for [`STSLICE`](#instr-stslice). | `18` |
| **`F400`** | `STDICT`<br/>`STOPTREF` | _`D b - b'`_ | Stores dictionary `D` into _Builder_ `b`, returing the resulting _Builder_ `b'`.<br/>In other words, if `D` is a cell, performs [`STONE`](#instr-stone) and [`STREF`](#instr-stref); if `D` is _Null_, performs [`NIP`](#instr-nip) and [`STZERO`](#instr-stzero); otherwise throws a type checking exception. | `26` |
| **`F401`** | `SKIPDICT`<br/>`SKIPOPTREF` | _`s - s'`_ | Equivalent to [`LDDICT`](#instr-lddict) [`NIP`](#instr-nip). | `26` |
| **`F402`** | `LDDICTS` | _`s - s' s''`_ | Loads (parses) a (_Slice_-represented) dictionary `s'` from _Slice_ `s`, and returns the remainder of `s` as `s''`.<br/>This is a “split function'' for all `HashmapE(n,X)` dictionary types. | `26` |
| **`F403`** | `PLDDICTS` | _`s - s'`_ | Preloads a (_Slice_-represented) dictionary `s'` from _Slice_ `s`.<br/>Approximately equivalent to [`LDDICTS`](#instr-lddicts) [`DROP`](#instr-drop). | `26` |
| **`F404`** | `LDDICT`<br/>`LDOPTREF` | _`s - D s'`_ | Loads (parses) a dictionary `D` from _Slice_ `s`, and returns the remainder of `s` as `s'`. May be applied to dictionaries or to values of arbitrary `(^Y)?` types. | `26` |
| **`F405`** | `PLDDICT`<br/>`PLDOPTREF` | _`s - D`_ | Preloads a dictionary `D` from _Slice_ `s`.<br/>Approximately equivalent to [`LDDICT`](#instr-lddict) [`DROP`](#instr-drop). | `26` |
| **`F406`** | `LDDICTQ` | _`s - D s' -1 or s 0`_ | A quiet version of [`LDDICT`](#instr-lddict). | `26` |
| **`F407`** | `PLDDICTQ` | _`s - D -1 or 0`_ | A quiet version of [`PLDDICT`](#instr-plddict). | `26` |
### 10.3 Get dictionary operations
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F40A`** | `DICTGET` | _`k D n - x -1 or 0`_ | Looks up key `k` (represented by a _Slice_, the first `0 <= n <= 1023` data bits of which are used as a key) in dictionary `D` of type `HashmapE(n,X)` with `n`-bit keys.<br/>On success, returns the value found as a _Slice_ `x`. |  |
| **`F40B`** | `DICTGETREF` | _`k D n - c -1 or 0`_ | Similar to [`DICTGET`](#instr-dictget), but with a [`LDREF`](#instr-ldref) [`ENDS`](#instr-ends) applied to `x` on success.<br/>This operation is useful for dictionaries of type `HashmapE(n,^Y)`. |  |
| **`F40C`** | `DICTIGET` | _`i D n - x -1 or 0`_ | Similar to [`DICTGET`](#instr-dictget), but with a signed (big-endian) `n`-bit _Integer_ `i` as a key. If `i` does not fit into `n` bits, returns `0`. If `i` is a `NaN`, throws an integer overflow exception. |  |
| **`F40D`** | `DICTIGETREF` | _`i D n - c -1 or 0`_ | Combines [`DICTIGET`](#instr-dictiget) with [`DICTGETREF`](#instr-dictgetref): it uses signed `n`-bit _Integer_ `i` as a key and returns a _Cell_ instead of a _Slice_ on success. |  |
| **`F40E`** | `DICTUGET` | _`i D n - x -1 or 0`_ | Similar to [`DICTIGET`](#instr-dictiget), but with _unsigned_ (big-endian) `n`-bit _Integer_ `i` used as a key. |  |
| **`F40F`** | `DICTUGETREF` | _`i D n - c -1 or 0`_ | Similar to [`DICTIGETREF`](#instr-dictigetref), but with an unsigned `n`-bit _Integer_ key `i`. |  |
### 10.4 Set/Replace/Add dictionary operations
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F412`** | `DICTSET` | _`x k D n - D'`_ | Sets the value associated with `n`-bit key `k` (represented by a _Slice_ as in [`DICTGET`](#instr-dictget)) in dictionary `D` (also represented by a _Slice_) to value `x` (again a _Slice_), and returns the resulting dictionary as `D'`. |  |
| **`F413`** | `DICTSETREF` | _`c k D n - D'`_ | Similar to [`DICTSET`](#instr-dictset), but with the value set to a reference to _Cell_ `c`. |  |
| **`F414`** | `DICTISET` | _`x i D n - D'`_ | Similar to [`DICTSET`](#instr-dictset), but with the key represented by a (big-endian) signed `n`-bit integer `i`. If `i` does not fit into `n` bits, a range check exception is generated. |  |
| **`F415`** | `DICTISETREF` | _`c i D n - D'`_ | Similar to [`DICTSETREF`](#instr-dictsetref), but with the key a signed `n`-bit integer as in [`DICTISET`](#instr-dictiset). |  |
| **`F416`** | `DICTUSET` | _`x i D n - D'`_ | Similar to [`DICTISET`](#instr-dictiset), but with `i` an _unsigned_ `n`-bit integer. |  |
| **`F417`** | `DICTUSETREF` | _`c i D n - D'`_ | Similar to [`DICTISETREF`](#instr-dictisetref), but with `i` unsigned. |  |
| **`F41A`** | `DICTSETGET` | _`x k D n - D' y -1 or D' 0`_ | Combines [`DICTSET`](#instr-dictset) with [`DICTGET`](#instr-dictget): it sets the value corresponding to key `k` to `x`, but also returns the old value `y` associated with the key in question, if present. |  |
| **`F41B`** | `DICTSETGETREF` | _`c k D n - D' c' -1 or D' 0`_ | Combines [`DICTSETREF`](#instr-dictsetref) with [`DICTGETREF`](#instr-dictgetref) similarly to [`DICTSETGET`](#instr-dictsetget). |  |
| **`F41C`** | `DICTISETGET` | _`x i D n - D' y -1 or D' 0`_ | [`DICTISETGET`](#instr-dictisetget), but with `i` a signed `n`-bit integer. |  |
| **`F41D`** | `DICTISETGETREF` | _`c i D n - D' c' -1 or D' 0`_ | [`DICTISETGETREF`](#instr-dictisetgetref), but with `i` a signed `n`-bit integer. |  |
| **`F41E`** | `DICTUSETGET` | _`x i D n - D' y -1 or D' 0`_ | [`DICTISETGET`](#instr-dictisetget), but with `i` an unsigned `n`-bit integer. |  |
| **`F41F`** | `DICTUSETGETREF` | _`c i D n - D' c' -1 or D' 0`_ | [`DICTISETGETREF`](#instr-dictisetgetref), but with `i` an unsigned `n`-bit integer. |  |
| **`F422`** | `DICTREPLACE` | _`x k D n - D' -1 or D 0`_ | A _Replace_ operation, which is similar to [`DICTSET`](#instr-dictset), but sets the value of key `k` in dictionary `D` to `x` only if the key `k` was already present in `D`. |  |
| **`F423`** | `DICTREPLACEREF` | _`c k D n - D' -1 or D 0`_ | A _Replace_ counterpart of [`DICTSETREF`](#instr-dictsetref). |  |
| **`F424`** | `DICTIREPLACE` | _`x i D n - D' -1 or D 0`_ | [`DICTREPLACE`](#instr-dictreplace), but with `i` a signed `n`-bit integer. |  |
| **`F425`** | `DICTIREPLACEREF` | _`c i D n - D' -1 or D 0`_ | [`DICTREPLACEREF`](#instr-dictreplaceref), but with `i` a signed `n`-bit integer. |  |
| **`F426`** | `DICTUREPLACE` | _`x i D n - D' -1 or D 0`_ | [`DICTREPLACE`](#instr-dictreplace), but with `i` an unsigned `n`-bit integer. |  |
| **`F427`** | `DICTUREPLACEREF` | _`c i D n - D' -1 or D 0`_ | [`DICTREPLACEREF`](#instr-dictreplaceref), but with `i` an unsigned `n`-bit integer. |  |
| **`F42A`** | `DICTREPLACEGET` | _`x k D n - D' y -1 or D 0`_ | A _Replace_ counterpart of [`DICTSETGET`](#instr-dictsetget): on success, also returns the old value associated with the key in question. |  |
| **`F42B`** | `DICTREPLACEGETREF` | _`c k D n - D' c' -1 or D 0`_ | A _Replace_ counterpart of [`DICTSETGETREF`](#instr-dictsetgetref). |  |
| **`F42C`** | `DICTIREPLACEGET` | _`x i D n - D' y -1 or D 0`_ | [`DICTREPLACEGET`](#instr-dictreplaceget), but with `i` a signed `n`-bit integer. |  |
| **`F42D`** | `DICTIREPLACEGETREF` | _`c i D n - D' c' -1 or D 0`_ | [`DICTREPLACEGETREF`](#instr-dictreplacegetref), but with `i` a signed `n`-bit integer. |  |
| **`F42E`** | `DICTUREPLACEGET` | _`x i D n - D' y -1 or D 0`_ | [`DICTREPLACEGET`](#instr-dictreplaceget), but with `i` an unsigned `n`-bit integer. |  |
| **`F42F`** | `DICTUREPLACEGETREF` | _`c i D n - D' c' -1 or D 0`_ | [`DICTREPLACEGETREF`](#instr-dictreplacegetref), but with `i` an unsigned `n`-bit integer. |  |
| **`F432`** | `DICTADD` | _`x k D n - D' -1 or D 0`_ | An _Add_ counterpart of [`DICTSET`](#instr-dictset): sets the value associated with key `k` in dictionary `D` to `x`, but only if it is not already present in `D`. |  |
| **`F433`** | `DICTADDREF` | _`c k D n - D' -1 or D 0`_ | An _Add_ counterpart of [`DICTSETREF`](#instr-dictsetref). |  |
| **`F434`** | `DICTIADD` | _`x i D n - D' -1 or D 0`_ | [`DICTADD`](#instr-dictadd), but with `i` a signed `n`-bit integer. |  |
| **`F435`** | `DICTIADDREF` | _`c i D n - D' -1 or D 0`_ | [`DICTADDREF`](#instr-dictaddref), but with `i` a signed `n`-bit integer. |  |
| **`F436`** | `DICTUADD` | _`x i D n - D' -1 or D 0`_ | [`DICTADD`](#instr-dictadd), but with `i` an unsigned `n`-bit integer. |  |
| **`F437`** | `DICTUADDREF` | _`c i D n - D' -1 or D 0`_ | [`DICTADDREF`](#instr-dictaddref), but with `i` an unsigned `n`-bit integer. |  |
| **`F43A`** | `DICTADDGET` | _`x k D n - D' -1 or D y 0`_ | An _Add_ counterpart of [`DICTSETGET`](#instr-dictsetget): sets the value associated with key `k` in dictionary `D` to `x`, but only if key `k` is not already present in `D`. Otherwise, just returns the old value `y` without changing the dictionary. |  |
| **`F43B`** | `DICTADDGETREF` | _`c k D n - D' -1 or D c' 0`_ | An _Add_ counterpart of [`DICTSETGETREF`](#instr-dictsetgetref). |  |
| **`F43C`** | `DICTIADDGET` | _`x i D n - D' -1 or D y 0`_ | [`DICTADDGET`](#instr-dictaddget), but with `i` a signed `n`-bit integer. |  |
| **`F43D`** | `DICTIADDGETREF` | _`c i D n - D' -1 or D c' 0`_ | [`DICTADDGETREF`](#instr-dictaddgetref), but with `i` a signed `n`-bit integer. |  |
| **`F43E`** | `DICTUADDGET` | _`x i D n - D' -1 or D y 0`_ | [`DICTADDGET`](#instr-dictaddget), but with `i` an unsigned `n`-bit integer. |  |
| **`F43F`** | `DICTUADDGETREF` | _`c i D n - D' -1 or D c' 0`_ | [`DICTADDGETREF`](#instr-dictaddgetref), but with `i` an unsigned `n`-bit integer. |  |
### 10.5 Builder-accepting variants of Set dictionary operations
The following primitives accept the new value as a _Builder_ `b` instead of a _Slice_ `x`.

| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F441`** | `DICTSETB` | _`b k D n - D'`_ |  |  |
| **`F442`** | `DICTISETB` | _`b i D n - D'`_ |  |  |
| **`F443`** | `DICTUSETB` | _`b i D n - D'`_ |  |  |
| **`F445`** | `DICTSETGETB` | _`b k D n - D' y -1 or D' 0`_ |  |  |
| **`F446`** | `DICTISETGETB` | _`b i D n - D' y -1 or D' 0`_ |  |  |
| **`F447`** | `DICTUSETGETB` | _`b i D n - D' y -1 or D' 0`_ |  |  |
| **`F449`** | `DICTREPLACEB` | _`b k D n - D' -1 or D 0`_ |  |  |
| **`F44A`** | `DICTIREPLACEB` | _`b i D n - D' -1 or D 0`_ |  |  |
| **`F44B`** | `DICTUREPLACEB` | _`b i D n - D' -1 or D 0`_ |  |  |
| **`F44D`** | `DICTREPLACEGETB` | _`b k D n - D' y -1 or D 0`_ |  |  |
| **`F44E`** | `DICTIREPLACEGETB` | _`b i D n - D' y -1 or D 0`_ |  |  |
| **`F44F`** | `DICTUREPLACEGETB` | _`b i D n - D' y -1 or D 0`_ |  |  |
| **`F451`** | `DICTADDB` | _`b k D n - D' -1 or D 0`_ |  |  |
| **`F452`** | `DICTIADDB` | _`b i D n - D' -1 or D 0`_ |  |  |
| **`F453`** | `DICTUADDB` | _`b i D n - D' -1 or D 0`_ |  |  |
| **`F455`** | `DICTADDGETB` | _`b k D n - D' -1 or D y 0`_ |  |  |
| **`F456`** | `DICTIADDGETB` | _`b i D n - D' -1 or D y 0`_ |  |  |
| **`F457`** | `DICTUADDGETB` | _`b i D n - D' -1 or D y 0`_ |  |  |
### 10.6 Delete dictionary operations
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F459`** | `DICTDEL` | _`k D n - D' -1 or D 0`_ | Deletes `n`-bit key, represented by a _Slice_ `k`, from dictionary `D`. If the key is present, returns the modified dictionary `D'` and the success flag `-1`. Otherwise, returns the original dictionary `D` and `0`. |  |
| **`F45A`** | `DICTIDEL` | _`i D n - D' ?`_ | A version of [`DICTDEL`](#instr-dictdel) with the key represented by a signed `n`-bit _Integer_ `i`. If `i` does not fit into `n` bits, simply returns `D` `0` (“key not found, dictionary unmodified''). |  |
| **`F45B`** | `DICTUDEL` | _`i D n - D' ?`_ | Similar to [`DICTIDEL`](#instr-dictidel), but with `i` an unsigned `n`-bit integer. |  |
| **`F462`** | `DICTDELGET` | _`k D n - D' x -1 or D 0`_ | Deletes `n`-bit key, represented by a _Slice_ `k`, from dictionary `D`. If the key is present, returns the modified dictionary `D'`, the original value `x` associated with the key `k` (represented by a _Slice_), and the success flag `-1`. Otherwise, returns the original dictionary `D` and `0`. |  |
| **`F463`** | `DICTDELGETREF` | _`k D n - D' c -1 or D 0`_ | Similar to [`DICTDELGET`](#instr-dictdelget), but with [`LDREF`](#instr-ldref) [`ENDS`](#instr-ends) applied to `x` on success, so that the value returned `c` is a _Cell_. |  |
| **`F464`** | `DICTIDELGET` | _`i D n - D' x -1 or D 0`_ | [`DICTDELGET`](#instr-dictdelget), but with `i` a signed `n`-bit integer. |  |
| **`F465`** | `DICTIDELGETREF` | _`i D n - D' c -1 or D 0`_ | [`DICTDELGETREF`](#instr-dictdelgetref), but with `i` a signed `n`-bit integer. |  |
| **`F466`** | `DICTUDELGET` | _`i D n - D' x -1 or D 0`_ | [`DICTDELGET`](#instr-dictdelget), but with `i` an unsigned `n`-bit integer. |  |
| **`F467`** | `DICTUDELGETREF` | _`i D n - D' c -1 or D 0`_ | [`DICTDELGETREF`](#instr-dictdelgetref), but with `i` an unsigned `n`-bit integer. |  |
### 10.7 "Maybe reference" dictionary operations
The following operations assume that a dictionary is used to store values `c?` of type _Maybe Cell_.  The representation is as follows: if `c?` is a _Cell_ , it is stored as a value with no data bits and exactly one reference to this _Cell_.  If `c?` is _Null_, then the corresponding key must be absent from the dictionary.

| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F469`** | `DICTGETOPTREF` | _`k D n - c^?`_ | A variant of [`DICTGETREF`](#instr-dictgetref) that returns _Null_ instead of the value `c^?` if the key `k` is absent from dictionary `D`. |  |
| **`F46A`** | `DICTIGETOPTREF` | _`i D n - c^?`_ | [`DICTGETOPTREF`](#instr-dictgetoptref), but with `i` a signed `n`-bit integer. If the key `i` is out of range, also returns _Null_. |  |
| **`F46B`** | `DICTUGETOPTREF` | _`i D n - c^?`_ | [`DICTGETOPTREF`](#instr-dictgetoptref), but with `i` an unsigned `n`-bit integer. If the key `i` is out of range, also returns _Null_. |  |
| **`F46D`** | `DICTSETGETOPTREF` | _`c^? k D n - D' ~c^?`_ | A variant of both [`DICTGETOPTREF`](#instr-dictgetoptref) and [`DICTSETGETREF`](#instr-dictsetgetref) that sets the value corresponding to key `k` in dictionary `D` to `c^?` (if `c^?` is _Null_, then the key is deleted instead), and returns the old value `~c^?` (if the key `k` was absent before, returns _Null_ instead). |  |
| **`F46E`** | `DICTISETGETOPTREF` | _`c^? i D n - D' ~c^?`_ | Similar to primitive [`DICTSETGETOPTREF`](#instr-dictsetgetoptref), but using signed `n`-bit _Integer_ `i` as a key. If `i` does not fit into `n` bits, throws a range checking exception. |  |
| **`F46F`** | `DICTUSETGETOPTREF` | _`c^? i D n - D' ~c^?`_ | Similar to primitive [`DICTSETGETOPTREF`](#instr-dictsetgetoptref), but using unsigned `n`-bit _Integer_ `i` as a key. |  |
### 10.8 Prefix code dictionary operations
These are some basic operations for constructing prefix code dictionaries.
These primitives are completely similar to their non-prefix code counterparts ([`DICTSET`](#instr-dictset) etc), with the obvious difference that even a _Set_ may fail in a prefix code dictionary, so a success flag must be returned by [`PFXDICTSET`](#instr-pfxdictset) as well.

| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F470`** | `PFXDICTSET` | _`x k D n - D' -1 or D 0`_ |  |  |
| **`F471`** | `PFXDICTREPLACE` | _`x k D n - D' -1 or D 0`_ |  |  |
| **`F472`** | `PFXDICTADD` | _`x k D n - D' -1 or D 0`_ |  |  |
| **`F473`** | `PFXDICTDEL` | _`k D n - D' -1 or D 0`_ |  |  |
### 10.9 Variants of GetNext and GetPrev operations
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F474`** | `DICTGETNEXT` | _`k D n - x' k' -1 or 0`_ | Computes the minimal key `k'` in dictionary `D` that is lexicographically greater than `k`, and returns `k'` (represented by a _Slice_) along with associated value `x'` (also represented by a _Slice_). |  |
| **`F475`** | `DICTGETNEXTEQ` | _`k D n - x' k' -1 or 0`_ | Similar to [`DICTGETNEXT`](#instr-dictgetnext), but computes the minimal key `k'` that is lexicographically greater than or equal to `k`. |  |
| **`F476`** | `DICTGETPREV` | _`k D n - x' k' -1 or 0`_ | Similar to [`DICTGETNEXT`](#instr-dictgetnext), but computes the maximal key `k'` lexicographically smaller than `k`. |  |
| **`F477`** | `DICTGETPREVEQ` | _`k D n - x' k' -1 or 0`_ | Similar to [`DICTGETPREV`](#instr-dictgetprev), but computes the maximal key `k'` lexicographically smaller than or equal to `k`. |  |
| **`F478`** | `DICTIGETNEXT` | _`i D n - x' i' -1 or 0`_ | Similar to [`DICTGETNEXT`](#instr-dictgetnext), but interprets all keys in dictionary `D` as big-endian signed `n`-bit integers, and computes the minimal key `i'` that is larger than _Integer_ `i` (which does not necessarily fit into `n` bits). |  |
| **`F479`** | `DICTIGETNEXTEQ` | _`i D n - x' i' -1 or 0`_ | Similar to [`DICTGETNEXTEQ`](#instr-dictgetnexteq), but interprets keys as signed `n`-bit integers. |  |
| **`F47A`** | `DICTIGETPREV` | _`i D n - x' i' -1 or 0`_ | Similar to [`DICTGETPREV`](#instr-dictgetprev), but interprets keys as signed `n`-bit integers. |  |
| **`F47B`** | `DICTIGETPREVEQ` | _`i D n - x' i' -1 or 0`_ | Similar to [`DICTGETPREVEQ`](#instr-dictgetpreveq), but interprets keys as signed `n`-bit integers. |  |
| **`F47C`** | `DICTUGETNEXT` | _`i D n - x' i' -1 or 0`_ | Similar to [`DICTGETNEXT`](#instr-dictgetnext), but interprets all keys in dictionary `D` as big-endian unsigned `n`-bit integers, and computes the minimal key `i'` that is larger than _Integer_ `i` (which does not necessarily fit into `n` bits, and is not necessarily non-negative). |  |
| **`F47D`** | `DICTUGETNEXTEQ` | _`i D n - x' i' -1 or 0`_ | Similar to [`DICTGETNEXTEQ`](#instr-dictgetnexteq), but interprets keys as unsigned `n`-bit integers. |  |
| **`F47E`** | `DICTUGETPREV` | _`i D n - x' i' -1 or 0`_ | Similar to [`DICTGETPREV`](#instr-dictgetprev), but interprets keys as unsigned `n`-bit integers. |  |
| **`F47F`** | `DICTUGETPREVEQ` | _`i D n - x' i' -1 or 0`_ | Similar to [`DICTGETPREVEQ`](#instr-dictgetpreveq), but interprets keys a unsigned `n`-bit integers. |  |
### 10.10 GetMin, GetMax, RemoveMin, RemoveMax operations
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F482`** | `DICTMIN` | _`D n - x k -1 or 0`_ | Computes the minimal key `k` (represented by a _Slice_ with `n` data bits) in dictionary `D`, and returns `k` along with the associated value `x`. |  |
| **`F483`** | `DICTMINREF` | _`D n - c k -1 or 0`_ | Similar to [`DICTMIN`](#instr-dictmin), but returns the only reference in the value as a _Cell_ `c`. |  |
| **`F484`** | `DICTIMIN` | _`D n - x i -1 or 0`_ | Similar to [`DICTMIN`](#instr-dictmin), but computes the minimal key `i` under the assumption that all keys are big-endian signed `n`-bit integers. Notice that the key and value returned may differ from those computed by [`DICTMIN`](#instr-dictmin) and [`DICTUMIN`](#instr-dictumin). |  |
| **`F485`** | `DICTIMINREF` | _`D n - c i -1 or 0`_ | Similar to [`DICTIMIN`](#instr-dictimin), but returns the only reference in the value. |  |
| **`F486`** | `DICTUMIN` | _`D n - x i -1 or 0`_ | Similar to [`DICTMIN`](#instr-dictmin), but returns the key as an unsigned `n`-bit _Integer_ `i`. |  |
| **`F487`** | `DICTUMINREF` | _`D n - c i -1 or 0`_ | Similar to [`DICTUMIN`](#instr-dictumin), but returns the only reference in the value. |  |
| **`F48A`** | `DICTMAX` | _`D n - x k -1 or 0`_ | Computes the maximal key `k` (represented by a _Slice_ with `n` data bits) in dictionary `D`, and returns `k` along with the associated value `x`. |  |
| **`F48B`** | `DICTMAXREF` | _`D n - c k -1 or 0`_ | Similar to [`DICTMAX`](#instr-dictmax), but returns the only reference in the value. |  |
| **`F48C`** | `DICTIMAX` | _`D n - x i -1 or 0`_ | Similar to [`DICTMAX`](#instr-dictmax), but computes the maximal key `i` under the assumption that all keys are big-endian signed `n`-bit integers. Notice that the key and value returned may differ from those computed by [`DICTMAX`](#instr-dictmax) and [`DICTUMAX`](#instr-dictumax). |  |
| **`F48D`** | `DICTIMAXREF` | _`D n - c i -1 or 0`_ | Similar to [`DICTIMAX`](#instr-dictimax), but returns the only reference in the value. |  |
| **`F48E`** | `DICTUMAX` | _`D n - x i -1 or 0`_ | Similar to [`DICTMAX`](#instr-dictmax), but returns the key as an unsigned `n`-bit _Integer_ `i`. |  |
| **`F48F`** | `DICTUMAXREF` | _`D n - c i -1 or 0`_ | Similar to [`DICTUMAX`](#instr-dictumax), but returns the only reference in the value. |  |
| **`F492`** | `DICTREMMIN` | _`D n - D' x k -1 or D 0`_ | Computes the minimal key `k` (represented by a _Slice_ with `n` data bits) in dictionary `D`, removes `k` from the dictionary, and returns `k` along with the associated value `x` and the modified dictionary `D'`. |  |
| **`F493`** | `DICTREMMINREF` | _`D n - D' c k -1 or D 0`_ | Similar to [`DICTREMMIN`](#instr-dictremmin), but returns the only reference in the value as a _Cell_ `c`. |  |
| **`F494`** | `DICTIREMMIN` | _`D n - D' x i -1 or D 0`_ | Similar to [`DICTREMMIN`](#instr-dictremmin), but computes the minimal key `i` under the assumption that all keys are big-endian signed `n`-bit integers. Notice that the key and value returned may differ from those computed by [`DICTREMMIN`](#instr-dictremmin) and [`DICTUREMMIN`](#instr-dicturemmin). |  |
| **`F495`** | `DICTIREMMINREF` | _`D n - D' c i -1 or D 0`_ | Similar to [`DICTIREMMIN`](#instr-dictiremmin), but returns the only reference in the value. |  |
| **`F496`** | `DICTUREMMIN` | _`D n - D' x i -1 or D 0`_ | Similar to [`DICTREMMIN`](#instr-dictremmin), but returns the key as an unsigned `n`-bit _Integer_ `i`. |  |
| **`F497`** | `DICTUREMMINREF` | _`D n - D' c i -1 or D 0`_ | Similar to [`DICTUREMMIN`](#instr-dicturemmin), but returns the only reference in the value. |  |
| **`F49A`** | `DICTREMMAX` | _`D n - D' x k -1 or D 0`_ | Computes the maximal key `k` (represented by a _Slice_ with `n` data bits) in dictionary `D`, removes `k` from the dictionary, and returns `k` along with the associated value `x` and the modified dictionary `D'`. |  |
| **`F49B`** | `DICTREMMAXREF` | _`D n - D' c k -1 or D 0`_ | Similar to [`DICTREMMAX`](#instr-dictremmax), but returns the only reference in the value as a _Cell_ `c`. |  |
| **`F49C`** | `DICTIREMMAX` | _`D n - D' x i -1 or D 0`_ | Similar to [`DICTREMMAX`](#instr-dictremmax), but computes the minimal key `i` under the assumption that all keys are big-endian signed `n`-bit integers. Notice that the key and value returned may differ from those computed by [`DICTREMMAX`](#instr-dictremmax) and [`DICTUREMMAX`](#instr-dicturemmax). |  |
| **`F49D`** | `DICTIREMMAXREF` | _`D n - D' c i -1 or D 0`_ | Similar to [`DICTIREMMAX`](#instr-dictiremmax), but returns the only reference in the value. |  |
| **`F49E`** | `DICTUREMMAX` | _`D n - D' x i -1 or D 0`_ | Similar to [`DICTREMMAX`](#instr-dictremmax), but returns the key as an unsigned `n`-bit _Integer_ `i`. |  |
| **`F49F`** | `DICTUREMMAXREF` | _`D n - D' c i -1 or D 0`_ | Similar to [`DICTUREMMAX`](#instr-dicturemmax), but returns the only reference in the value. |  |
### 10.11 Special Get dictionary and prefix code dictionary operations and constant dictionaries
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F4A0`** | `DICTIGETJMP` | _`i D n - `_ | Similar to [`DICTIGET`](#instr-dictiget), but with `x` [`BLESS`](#instr-bless)ed into a continuation with a subsequent [`JMPX`](#instr-jmpx) to it on success. On failure, does nothing. This is useful for implementing `switch`/`case` constructions. |  |
| **`F4A1`** | `DICTUGETJMP` | _`i D n - `_ | Similar to [`DICTIGETJMP`](#instr-dictigetjmp), but performs [`DICTUGET`](#instr-dictuget) instead of [`DICTIGET`](#instr-dictiget). |  |
| **`F4A2`** | `DICTIGETEXEC` | _`i D n - `_ | Similar to [`DICTIGETJMP`](#instr-dictigetjmp), but with [`EXECUTE`](#instr-execute) instead of [`JMPX`](#instr-jmpx). |  |
| **`F4A3`** | `DICTUGETEXEC` | _`i D n - `_ | Similar to [`DICTUGETJMP`](#instr-dictugetjmp), but with [`EXECUTE`](#instr-execute) instead of [`JMPX`](#instr-jmpx). |  |
| **`F4A6_n`** | `[ref] [n] DICTPUSHCONST` | _` - D n`_ | Pushes a non-empty constant dictionary `D` (as a `Cell^?`) along with its key length `0 <= n <= 1023`, stored as a part of the instruction. The dictionary itself is created from the first of remaining references of the current continuation. In this way, the complete [`DICTPUSHCONST`](#instr-dictpushconst) instruction can be obtained by first serializing `xF4A4_`, then the non-empty dictionary itself (one `1` bit and a cell reference), and then the unsigned 10-bit integer `n` (as if by a `STU 10` instruction). An empty dictionary can be pushed by a [`NEWDICT`](#instr-newdict) primitive instead. | `34` |
| **`F4A8`** | `PFXDICTGETQ` | _`s D n - s' x s'' -1 or s 0`_ | Looks up the unique prefix of _Slice_ `s` present in the prefix code dictionary represented by `Cell^?` `D` and `0 <= n <= 1023`. If found, the prefix of `s` is returned as `s'`, and the corresponding value (also a _Slice_) as `x`. The remainder of `s` is returned as a _Slice_ `s''`. If no prefix of `s` is a key in prefix code dictionary `D`, returns the unchanged `s` and a zero flag to indicate failure. |  |
| **`F4A9`** | `PFXDICTGET` | _`s D n - s' x s''`_ | Similar to [`PFXDICTGET`](#instr-pfxdictget), but throws a cell deserialization failure exception on failure. |  |
| **`F4AA`** | `PFXDICTGETJMP` | _`s D n - s' s'' or s`_ | Similar to [`PFXDICTGETQ`](#instr-pfxdictgetq), but on success [`BLESS`](#instr-bless)es the value `x` into a _Continuation_ and transfers control to it as if by a [`JMPX`](#instr-jmpx). On failure, returns `s` unchanged and continues execution. |  |
| **`F4AB`** | `PFXDICTGETEXEC` | _`s D n - s' s''`_ | Similar to [`PFXDICTGETJMP`](#instr-pfxdictgetjmp), but `EXEC`utes the continuation found instead of jumping to it. On failure, throws a cell deserialization exception. |  |
| **`F4AE_n`** | `[ref] [n] PFXDICTCONSTGETJMP`<br/>`[ref] [n] PFXDICTSWITCH` | _`s - s' s'' or s`_ | Combines [`[n] DICTPUSHCONST`](#instr-dictpushconst) for `0 <= n <= 1023` with [`PFXDICTGETJMP`](#instr-pfxdictgetjmp). |  |
| **`F4BC`** | `DICTIGETJMPZ` | _`i D n - i or nothing`_ | A variant of [`DICTIGETJMP`](#instr-dictigetjmp) that returns index `i` on failure. |  |
| **`F4BD`** | `DICTUGETJMPZ` | _`i D n - i or nothing`_ | A variant of [`DICTUGETJMP`](#instr-dictugetjmp) that returns index `i` on failure. |  |
| **`F4BE`** | `DICTIGETEXECZ` | _`i D n - i or nothing`_ | A variant of [`DICTIGETEXEC`](#instr-dictigetexec) that returns index `i` on failure. |  |
| **`F4BF`** | `DICTUGETEXECZ` | _`i D n - i or nothing`_ | A variant of [`DICTUGETEXEC`](#instr-dictugetexec) that returns index `i` on failure. |  |
### 10.12 SubDict dictionary operations
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F4B1`** | `SUBDICTGET` | _`k l D n - D'`_ | Constructs a subdictionary consisting of all keys beginning with prefix `k` (represented by a _Slice_, the first `0 <= l <= n <= 1023` data bits of which are used as a key) of length `l` in dictionary `D` of type `HashmapE(n,X)` with `n`-bit keys. On success, returns the new subdictionary of the same type `HashmapE(n,X)` as a _Slice_ `D'`. |  |
| **`F4B2`** | `SUBDICTIGET` | _`x l D n - D'`_ | Variant of [`SUBDICTGET`](#instr-subdictget) with the prefix represented by a signed big-endian `l`-bit _Integer_ `x`, where necessarily `l <= 257`. |  |
| **`F4B3`** | `SUBDICTUGET` | _`x l D n - D'`_ | Variant of [`SUBDICTGET`](#instr-subdictget) with the prefix represented by an unsigned big-endian `l`-bit _Integer_ `x`, where necessarily `l <= 256`. |  |
| **`F4B5`** | `SUBDICTRPGET` | _`k l D n - D'`_ | Similar to [`SUBDICTGET`](#instr-subdictget), but removes the common prefix `k` from all keys of the new dictionary `D'`, which becomes of type `HashmapE(n-l,X)`. |  |
| **`F4B6`** | `SUBDICTIRPGET` | _`x l D n - D'`_ | Variant of [`SUBDICTRPGET`](#instr-subdictrpget) with the prefix represented by a signed big-endian `l`-bit _Integer_ `x`, where necessarily `l <= 257`. |  |
| **`F4B7`** | `SUBDICTURPGET` | _`x l D n - D'`_ | Variant of [`SUBDICTRPGET`](#instr-subdictrpget) with the prefix represented by an unsigned big-endian `l`-bit _Integer_ `x`, where necessarily `l <= 256`. |  |

## 11 Application-specific primitives
### 11.1 Gas-related primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F800`** | `ACCEPT` | _`-`_ | Sets current gas limit `g_l` to its maximal allowed value `g_m`, and resets the gas credit `g_c` to zero, decreasing the value of `g_r` by `g_c` in the process.<br/>In other words, the current smart contract agrees to buy some gas to finish the current transaction. This action is required to process external messages, which bring no value (hence no gas) with themselves. | `26` |
| **`F801`** | `SETGASLIMIT` | _`g - `_ | Sets current gas limit `g_l` to the minimum of `g` and `g_m`, and resets the gas credit `g_c` to zero. If the gas consumed so far (including the present instruction) exceeds the resulting value of `g_l`, an (unhandled) out of gas exception is thrown before setting new gas limits. Notice that [`SETGASLIMIT`](#instr-setgaslimit) with an argument `g >= 2^63-1` is equivalent to [`ACCEPT`](#instr-accept). | `26` |
| **`F80F`** | `COMMIT` | _`-`_ | Commits the current state of registers `c4` (“persistent data'') and `c5` (“actions'') so that the current execution is considered “successful'' with the saved values even if an exception is thrown later. | `26` |
### 11.2 Pseudo-random number generator primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F810`** | `RANDU256` | _`- x`_ | Generates a new pseudo-random unsigned 256-bit _Integer_ `x`. The algorithm is as follows: if `r` is the old value of the random seed, considered as a 32-byte array (by constructing the big-endian representation of an unsigned 256-bit integer), then its `sha512(r)` is computed; the first 32 bytes of this hash are stored as the new value `r'` of the random seed, and the remaining 32 bytes are returned as the next random value `x`. | `26+\|c7\|+\|c1_1\|` |
| **`F811`** | `RAND` | _`y - z`_ | Generates a new pseudo-random integer `z` in the range `0...y-1` (or `y...-1`, if `y<0`). More precisely, an unsigned random value `x` is generated as in `RAND256U`; then `z:=floor(x*y/2^256)` is computed.<br/>Equivalent to [`RANDU256`](#instr-randu256) [`256 MULRSHIFT`](#instr-mulrshift-var). | `26+\|c7\|+\|c1_1\|` |
| **`F814`** | `SETRAND` | _`x - `_ | Sets the random seed to unsigned 256-bit _Integer_ `x`. | `26+\|c7\|+\|c1_1\|` |
| **`F815`** | `ADDRAND`<br/>`RANDOMIZE` | _`x - `_ | Mixes unsigned 256-bit _Integer_ `x` into the random seed `r` by setting the random seed to `Sha` of the concatenation of two 32-byte strings: the first with the big-endian representation of the old seed `r`, and the second with the big-endian representation of `x`. | `26` |
### 11.3 Configuration primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F82i`** | `[i] GETPARAM` | _` - x`_ | Returns the `i`-th parameter from the _Tuple_ provided at `c7` for `0 <= i <= 15`. Equivalent to [`c7 PUSHCTR`](#instr-pushctr) [`FIRST`](#instr-first) [`[i] INDEX`](#instr-index).<br/>If one of these internal operations fails, throws an appropriate type checking or range checking exception. | `26` |
| **`F823`** | `NOW` | _` - x`_ | Returns the current Unix time as an _Integer_. If it is impossible to recover the requested value starting from `c7`, throws a type checking or range checking exception as appropriate.<br/>Equivalent to [`3 GETPARAM`](#instr-getparam). | `26` |
| **`F824`** | `BLOCKLT` | _` - x`_ | Returns the starting logical time of the current block.<br/>Equivalent to [`4 GETPARAM`](#instr-getparam). | `26` |
| **`F825`** | `LTIME` | _` - x`_ | Returns the logical time of the current transaction.<br/>Equivalent to [`5 GETPARAM`](#instr-getparam). | `26` |
| **`F826`** | `RANDSEED` | _` - x`_ | Returns the current random seed as an unsigned 256-bit _Integer_.<br/>Equivalent to [`6 GETPARAM`](#instr-getparam). | `26` |
| **`F827`** | `BALANCE` | _` - t`_ | Returns the remaining balance of the smart contract as a _Tuple_ consisting of an _Integer_ (the remaining Gram balance in nanograms) and a _Maybe Cell_ (a dictionary with 32-bit keys representing the balance of “extra currencies'').<br/>Equivalent to [`7 GETPARAM`](#instr-getparam).<br/>Note that `RAW` primitives such as [`SENDRAWMSG`](#instr-sendrawmsg) do not update this field. | `26` |
| **`F828`** | `MYADDR` | _` - s`_ | Returns the internal address of the current smart contract as a _Slice_ with a `MsgAddressInt`. If necessary, it can be parsed further using primitives such as [`PARSEMSGADDR`](#instr-parsemsgaddr) or [`REWRITESTDADDR`](#instr-rewritestdaddr).<br/>Equivalent to [`8 GETPARAM`](#instr-getparam). | `26` |
| **`F829`** | `CONFIGROOT` | _` - D`_ | Returns the _Maybe Cell_ `D` with the current global configuration dictionary. Equivalent to `9 GETPARAM `. | `26` |
| **`F830`** | `CONFIGDICT` | _` - D 32`_ | Returns the global configuration dictionary along with its key length (32).<br/>Equivalent to [`CONFIGROOT`](#instr-configroot) [`32 PUSHINT`](#instr-pushint-4). | `26` |
| **`F832`** | `CONFIGPARAM` | _`i - c -1 or 0`_ | Returns the value of the global configuration parameter with integer index `i` as a _Cell_ `c`, and a flag to indicate success.<br/>Equivalent to [`CONFIGDICT`](#instr-configdict) [`DICTIGETREF`](#instr-dictigetref). |  |
| **`F833`** | `CONFIGOPTPARAM` | _`i - c^?`_ | Returns the value of the global configuration parameter with integer index `i` as a _Maybe Cell_ `c^?`.<br/>Equivalent to [`CONFIGDICT`](#instr-configdict) [`DICTIGETOPTREF`](#instr-dictigetoptref). |  |
### 11.4 Global variable primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F840`** | `GETGLOBVAR` | _`k - x`_ | Returns the `k`-th global variable for `0 <= k < 255`.<br/>Equivalent to [`c7 PUSHCTR`](#instr-pushctr) [`SWAP`](#instr-swap) [`INDEXVARQ`](#instr-indexvarq). | `26` |
| **`F85_k`** | `[k] GETGLOB` | _` - x`_ | Returns the `k`-th global variable for `1 <= k <= 31`.<br/>Equivalent to [`c7 PUSHCTR`](#instr-pushctr) [`[k] INDEXQ`](#instr-indexq). | `26` |
| **`F860`** | `SETGLOBVAR` | _`x k - `_ | Assigns `x` to the `k`-th global variable for `0 <= k < 255`.<br/>Equivalent to [`c7 PUSHCTR`](#instr-pushctr) [`ROTREV`](#instr-rotrev) [`SETINDEXVARQ`](#instr-setindexvarq) [`c7 POPCTR`](#instr-popctr). | `26+\|c7’\|` |
| **`F87_k`** | `[k] SETGLOB` | _`x - `_ | Assigns `x` to the `k`-th global variable for `1 <= k <= 31`.<br/>Equivalent to [`c7 PUSHCTR`](#instr-pushctr) [`SWAP`](#instr-swap) [`k SETINDEXQ`](#instr-setindexq) [`c7 POPCTR`](#instr-popctr). | `26+\|c7’\|` |
### 11.5 Hashing and cryptography primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F900`** | `HASHCU` | _`c - x`_ | Computes the representation hash of a _Cell_ `c` and returns it as a 256-bit unsigned integer `x`. Useful for signing and checking signatures of arbitrary entities represented by a tree of cells. | `26` |
| **`F901`** | `HASHSU` | _`s - x`_ | Computes the hash of a _Slice_ `s` and returns it as a 256-bit unsigned integer `x`. The result is the same as if an ordinary cell containing only data and references from `s` had been created and its hash computed by [`HASHCU`](#instr-hashcu). | `526` |
| **`F902`** | `SHA256U` | _`s - x`_ | Computes `Sha` of the data bits of _Slice_ `s`. If the bit length of `s` is not divisible by eight, throws a cell underflow exception. The hash value is returned as a 256-bit unsigned integer `x`. | `26` |
| **`F910`** | `CHKSIGNU` | _`h s k - ?`_ | Checks the Ed25519-signature `s` of a hash `h` (a 256-bit unsigned integer, usually computed as the hash of some data) using public key `k` (also represented by a 256-bit unsigned integer).<br/>The signature `s` must be a _Slice_ containing at least 512 data bits; only the first 512 bits are used. The result is `-1` if the signature is valid, `0` otherwise.<br/>Notice that [`CHKSIGNU`](#instr-chksignu) is equivalent to [`ROT`](#instr-rot) [`NEWC`](#instr-newc) [`256 STU`](#instr-stu) [`ENDC`](#instr-endc) [`ROTREV`](#instr-rotrev) [`CHKSIGNS`](#instr-chksigns), i.e., to [`CHKSIGNS`](#instr-chksigns) with the first argument `d` set to 256-bit _Slice_ containing `h`. Therefore, if `h` is computed as the hash of some data, these data are hashed _twice_, the second hashing occurring inside [`CHKSIGNS`](#instr-chksigns). | `26` |
| **`F911`** | `CHKSIGNS` | _`d s k - ?`_ | Checks whether `s` is a valid Ed25519-signature of the data portion of _Slice_ `d` using public key `k`, similarly to [`CHKSIGNU`](#instr-chksignu). If the bit length of _Slice_ `d` is not divisible by eight, throws a cell underflow exception. The verification of Ed25519 signatures is the standard one, with `Sha` used to reduce `d` to the 256-bit number that is actually signed. | `26` |
### 11.6 Miscellaneous primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`F940`** | `CDATASIZEQ` | _`c n - x y z -1 or 0`_ | Recursively computes the count of distinct cells `x`, data bits `y`, and cell references `z` in the dag rooted at _Cell_ `c`, effectively returning the total storage used by this dag taking into account the identification of equal cells. The values of `x`, `y`, and `z` are computed by a depth-first traversal of this dag, with a hash table of visited cell hashes used to prevent visits of already-visited cells. The total count of visited cells `x` cannot exceed non-negative _Integer_ `n`; otherwise the computation is aborted before visiting the `(n+1)`-st cell and a zero is returned to indicate failure. If `c` is _Null_, returns `x=y=z=0`. |  |
| **`F941`** | `CDATASIZE` | _`c n - x y z`_ | A non-quiet version of [`CDATASIZEQ`](#instr-cdatasizeq) that throws a cell overflow exception (8) on failure. |  |
| **`F942`** | `SDATASIZEQ` | _`s n - x y z -1 or 0`_ | Similar to [`CDATASIZEQ`](#instr-cdatasizeq), but accepting a _Slice_ `s` instead of a _Cell_. The returned value of `x` does not take into account the cell that contains the slice `s` itself; however, the data bits and the cell references of `s` are accounted for in `y` and `z`. |  |
| **`F943`** | `SDATASIZE` | _`s n - x y z`_ | A non-quiet version of [`SDATASIZEQ`](#instr-sdatasizeq) that throws a cell overflow exception (8) on failure. |  |
### 11.7 Currency manipulation primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`FA00`** | `LDGRAMS`<br/>`LDVARUINT16` | _`s - x s'`_ | Loads (deserializes) a `Gram` or `VarUInteger 16` amount from _Slice_ `s`, and returns the amount as _Integer_ `x` along with the remainder `s'` of `s`. The expected serialization of `x` consists of a 4-bit unsigned big-endian integer `l`, followed by an `8l`-bit unsigned big-endian representation of `x`.<br/>The net effect is approximately equivalent to [`4 LDU`](#instr-ldu) [`SWAP`](#instr-swap) [`3 LSHIFT#`](#instr-lshift) [`LDUX`](#instr-ldux). | `26` |
| **`FA01`** | `LDVARINT16` | _`s - x s'`_ | Similar to [`LDVARUINT16`](#instr-ldgrams), but loads a _signed_ _Integer_ `x`.<br/>Approximately equivalent to [`4 LDU`](#instr-ldu) [`SWAP`](#instr-swap) [`3 LSHIFT#`](#instr-lshift) [`LDIX`](#instr-ldix). | `26` |
| **`FA02`** | `STGRAMS`<br/>`STVARUINT16` | _`b x - b'`_ | Stores (serializes) an _Integer_ `x` in the range `0...2^120-1` into _Builder_ `b`, and returns the resulting _Builder_ `b'`. The serialization of `x` consists of a 4-bit unsigned big-endian integer `l`, which is the smallest integer `l>=0`, such that `x<2^(8l)`, followed by an `8l`-bit unsigned big-endian representation of `x`. If `x` does not belong to the supported range, a range check exception is thrown. | `26` |
| **`FA03`** | `STVARINT16` | _`b x - b'`_ | Similar to [`STVARUINT16`](#instr-stgrams), but serializes a _signed_ _Integer_ `x` in the range `-2^119...2^119-1`. | `26` |
### 11.8 Message and address manipulation primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`FA40`** | `LDMSGADDR` | _`s - s' s''`_ | Loads from _Slice_ `s` the only prefix that is a valid `MsgAddress`, and returns both this prefix `s'` and the remainder `s''` of `s` as slices. | `26` |
| **`FA41`** | `LDMSGADDRQ` | _`s - s' s'' -1 or s 0`_ | A quiet version of [`LDMSGADDR`](#instr-ldmsgaddr): on success, pushes an extra `-1`; on failure, pushes the original `s` and a zero. | `26` |
| **`FA42`** | `PARSEMSGADDR` | _`s - t`_ | Decomposes _Slice_ `s` containing a valid `MsgAddress` into a _Tuple_ `t` with separate fields of this `MsgAddress`. If `s` is not a valid `MsgAddress`, a cell deserialization exception is thrown. | `26` |
| **`FA43`** | `PARSEMSGADDRQ` | _`s - t -1 or 0`_ | A quiet version of [`PARSEMSGADDR`](#instr-parsemsgaddr): returns a zero on error instead of throwing an exception. | `26` |
| **`FA44`** | `REWRITESTDADDR` | _`s - x y`_ | Parses _Slice_ `s` containing a valid `MsgAddressInt` (usually a `msg_addr_std`), applies rewriting from the `anycast` (if present) to the same-length prefix of the address, and returns both the workchain `x` and the 256-bit address `y` as integers. If the address is not 256-bit, or if `s` is not a valid serialization of `MsgAddressInt`, throws a cell deserialization exception. | `26` |
| **`FA45`** | `REWRITESTDADDRQ` | _`s - x y -1 or 0`_ | A quiet version of primitive [`REWRITESTDADDR`](#instr-rewritestdaddr). | `26` |
| **`FA46`** | `REWRITEVARADDR` | _`s - x s'`_ | A variant of [`REWRITESTDADDR`](#instr-rewritestdaddr) that returns the (rewritten) address as a _Slice_ `s`, even if it is not exactly 256 bit long (represented by a `msg_addr_var`). | `26` |
| **`FA47`** | `REWRITEVARADDRQ` | _`s - x s' -1 or 0`_ | A quiet version of primitive [`REWRITEVARADDR`](#instr-rewritevaraddr). | `26` |
### 11.9 Outbound message and output action primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`FB00`** | `SENDRAWMSG` | _`c x - `_ | Sends a raw message contained in _Cell `c`_, which should contain a correctly serialized object `Message X`, with the only exception that the source address is allowed to have dummy value `addr_none` (to be automatically replaced with the current smart-contract address), and `ihr_fee`, `fwd_fee`, `created_lt` and `created_at` fields can have arbitrary values (to be rewritten with correct values during the action phase of the current transaction). Integer parameter `x` contains the flags. Currently `x=0` is used for ordinary messages; `x=128` is used for messages that are to carry all the remaining balance of the current smart contract (instead of the value originally indicated in the message); `x=64` is used for messages that carry all the remaining value of the inbound message in addition to the value initially indicated in the new message (if bit 0 is not set, the gas fees are deducted from this amount); `x'=x+1` means that the sender wants to pay transfer fees separately; `x'=x+2` means that any errors arising while processing this message during the action phase should be ignored. Finally, `x'=x+32` means that the current account must be destroyed if its resulting balance is zero. This flag is usually employed together with `+128`. | `526` |
| **`FB02`** | `RAWRESERVE` | _`x y - `_ | Creates an output action which would reserve exactly `x` nanograms (if `y=0`), at most `x` nanograms (if `y=2`), or all but `x` nanograms (if `y=1` or `y=3`), from the remaining balance of the account. It is roughly equivalent to creating an outbound message carrying `x` nanograms (or `b-x` nanograms, where `b` is the remaining balance) to oneself, so that the subsequent output actions would not be able to spend more money than the remainder. Bit `+2` in `y` means that the external action does not fail if the specified amount cannot be reserved; instead, all remaining balance is reserved. Bit `+8` in `y` means `x:=-x` before performing any further actions. Bit `+4` in `y` means that `x` is increased by the original balance of the current account (before the compute phase), including all extra currencies, before performing any other checks and actions. Currently `x` must be a non-negative integer, and `y` must be in the range `0...15`. | `526` |
| **`FB03`** | `RAWRESERVEX` | _`x D y - `_ | Similar to [`RAWRESERVE`](#instr-rawreserve), but also accepts a dictionary `D` (represented by a _Cell_ or _Null_) with extra currencies. In this way currencies other than Grams can be reserved. | `526` |
| **`FB04`** | `SETCODE` | _`c - `_ | Creates an output action that would change this smart contract code to that given by _Cell_ `c`. Notice that this change will take effect only after the successful termination of the current run of the smart contract. | `526` |
| **`FB06`** | `SETLIBCODE` | _`c x - `_ | Creates an output action that would modify the collection of this smart contract libraries by adding or removing library with code given in _Cell_ `c`. If `x=0`, the library is actually removed if it was previously present in the collection (if not, this action does nothing). If `x=1`, the library is added as a private library, and if `x=2`, the library is added as a public library (and becomes available to all smart contracts if the current smart contract resides in the masterchain); if the library was present in the collection before, its public/private status is changed according to `x`. Values of `x` other than `0...2` are invalid. | `526` |
| **`FB07`** | `CHANGELIB` | _`h x - `_ | Creates an output action similarly to [`SETLIBCODE`](#instr-setlibcode), but instead of the library code accepts its hash as an unsigned 256-bit integer `h`. If `x!=0` and the library with hash `h` is absent from the library collection of this smart contract, this output action will fail. | `526` |

## 12 Debug primitives
Opcodes beginning with `FE` are reserved for the debug primitives. These primitives have known fixed operation length and behave as (multibyte) [`NOP`](#instr-nop) operations.

However, when invoked in a TVM instance with debug mode enabled, these primitives can produce a specific output into the text debug log of the TVM instance, never affecting the TVM state.

[`DEBUG`](#instr-debug) and [`DEBUGSTR`](#instr-debugstr) are the two debug primitives, they cover all opcodes that start with `FE`.
Other primitives listed here have opcodes from the same set. When debug is enabled, they have their specified effects. When debug is disabled, they behave as [`NOP`](#instr-nop).

| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`FEnn`** | `{nn} DEBUG` | _`-`_ | `0 <= nn < 240` | `26` |
| **`FEFnssss`** | `{string} DEBUGSTR`<br/>`{string} {x} DEBUGSTRI` | _`-`_ | `0 <= n < 16`. Length of `ssss` is `n+1` bytes.<br/>`{string}` is a [string literal](https://github.com/Piterden/TON-docs/blob/master/Fift.%20A%20Brief%20Introduction.md#user-content-29-string-literals).<br/>[`DEBUGSTR`](#instr-debugstr): `ssss` is the given string.<br/>[`DEBUGSTRI`](#instr-debugstr): `ssss` is one-byte integer `0 <= x <= 255` followed by the given string. | `26` |
| **`FE00`** | `DUMPSTK` | _`-`_ | Dumps the stack (at most the top 255 values) and shows the total stack depth. | `26` |
| **`FE2i`** | `s[i] DUMP` | _`-`_ | Dumps `s[i]`. | `26` |

## 13 Codepage primitives
| xxxxxxx<br/>Opcode | xxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description | xxxx<br/>Gas |
|:-|:-|:-|:-|:-|
| **`FFnn`** | `[nn] SETCP` | _`-`_ | Selects TVM codepage `0 <= nn < 240`. If the codepage is not supported, throws an invalid opcode exception. | `26` |
| **`FF00`** | `SETCP0` | _`-`_ | Selects TVM (test) codepage zero as described in this document. | `26` |
| **`FFFz`** | `[z-16] SETCP` | _`-`_ | Selects TVM codepage `z-16` for `1 <= z <= 15`. Negative codepages `-13...-1` are reserved for restricted versions of TVM needed to validate runs of TVM in other codepages. Negative codepage `-14` is reserved for experimental codepages, not necessarily compatible between different TVM implementations, and should be disabled in the production versions of TVM. | `26` |
| **`FFF0`** | `SETCPX` | _`c - `_ | Selects codepage `c` with `-2^15 <= c < 2^15` passed in the top of the stack. | `26` |

