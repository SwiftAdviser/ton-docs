# Fift deep dive

A high-level stack-based language Fift is used for local manipulation with cells and other TVM primitives, mostly for converting TVM assembly code into contract code bag-of-cells.

:::caution
This section describes interacting with TON-specific features at **very** low level.
Serious understanding of stack languages' basics required.
:::

## Simple arithmetic
You are able to use Fift interpreter as calculator, writing in expressions in [reverse Polish notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation).
```
6 17 17 * * 289 + .
2023 ok
```

## Standard output
```
27 emit ."[30;1mgrey text" 27 emit ."[37m"
grey text ok
```
`emit` takes number from top of stack and prints Unicode character with the specified code into stdout.
`."..."` prints constant string.

## Defining functions (Fift words)
The main way of defining a word is to enclose its effects in curly braces then write `:` and word name.
```
{ minmax drop } : min
{ minmax nip } : max
```
> Fift.fif

Though, there are several *defining words*, not only `:`. They're different in the sense words defined with some of them are **active** (work inside curly braces) and some are **prefix** (don't require space character to be after them):
```
{ bl word 1 2 ' (create) } "::" 1 (create)
{ bl word 0 2 ' (create) } :: :
{ bl word 2 2 ' (create) } :: :_
{ bl word 3 2 ' (create) } :: ::_
{ bl word 0 (create) } : create
```
> Fift.fif

## Conditional execution
Code blocks (those delimited by curly braces) can be executed, either conditionally or unconditionally.
```
{ { ."true " } { ."false " } cond } : ?.   4 5 = ?.  4 5 < ?.
false true  ok
{ ."hello " } execute ."world"
hello world ok
```

## Loops
```
// ( l c -- l')  deletes first c elements from list l
{ ' safe-cdr swap times } : list-delete-first
```
> GetOpt.fif

Loop word `times` takes two arguments - let's call them `cont` and `n` - and executes `cont` `n` times.
Here `list-delete-first` takes continuation of `safe-cdr` (command deleting head from Lisp-style list), places it under `c` and then `c` times removes head from list present on stack.

There are also words `while` and `until`.

## Comments
```
{ 0 word drop 0 'nop } :: //
{ char " word 1 { swap { abort } if drop } } ::_ abort"
{ { bl word dup "" $= abort"comment extends after end of file" "*/" $= } until 0 'nop } :: /*
```
> Fift.fif

Comments are defined in `Fift.fif`. Single-line comment starts with `//` and continues to the end of line; multiline comment starts with `/*` and ends with `*/`.

Let's understand why they work so.  
Fift program is essentially sequence of words, each of those transforming stack in some way or defining new words. First line of `Fift.fif` (code shown above) is declaration of new word `//`.
Comments have to work even when defining new words, so they must work in nested environment. That's why they are defined as **active** words, by means of `::`. Actions of the word being created are listed in the curly braces:
1. `0`: zero is pushed onto stack
2. `word`: this command reads chars until one equal to top of stack is reached and pushes the data read as String. Zero is special case: here `word` skips leading spaces and then reads until the end of the current input line.
3. `drop`: top element (comment data) is dropped from stack.
4. `0`: zero is pushed onto stack again - number of results, used because word is defined with `::`.
5. `'nop` pushes execution token doing nothing when called. It's pretty much equivalent to `{ nop }`.

## Using Fift for defining TVM assembly codes
```
x{00} @Defop NOP
{ 1 ' @addop does create } : @Defop
{ tuck sbitrefs @ensurebitrefs swap s, } : @addop
{ @havebitrefs ' @| ifnot } : @ensurebitrefs
{ 2 pick brembitrefs 1- 2x<= } : @havebitrefs
{ rot >= -rot <= and } : 2x<=
...
```
> Asm.fif (lines order reversed)

`@Defop` takes care of checking if there is enough space for opcode (`@havebitrefs`), and if there is not, it goes on writing to another builder (`@|`; also known as implicit jump). That's why you generally don't want to write `x{A988} s,` as an opcode: there could be insufficient space to place this opcode, so compilation would fail; you should write `x{A988} @addop` instead.

You may use Fift for including big bag-of-cells into contract:
```
<b 8 4 u, 8 4 u, "fift/blob.boc" file>B B>boc ref, b> <s @Defop LDBLOB
```
This command defines opcode which, when being included into program, writes `x{88}` (`PUSHREF`) and a reference to provided bag-of-cells. So when `LDBLOB` instruction is ran, it pushes the cell to TVM stack.

## Special features

- Ed25519 cryptography
  - newkeypair - generates private-public key pair
  - priv>pub   - generates public key from private
  - ed25519_sign[_uint] - generates signature given data and private key
  - ed25519_chksign     - checks Ed25519 signature
- Interaction with TVM
  - runvmcode and similar - invokes TVM with code slice taken from stack
- Writing BOC into files:
  `boc>B ".../contract.boc" B>file`

## Continue learning

 - [Fift: A Brief Introduction](https://ton.org/docs/fiftbase.pdf) by Nikolai Durov
