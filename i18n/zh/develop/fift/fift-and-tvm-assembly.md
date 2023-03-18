# Fift and TVM assembly

Fift is stack-based programming language that has TON-specific features and therefore can work with cells. TVM assembly is also a stack-based programming language, also specific to TON, and it also can work with cells. So what's the difference between them?

## The difference

Fift is executed **at compile-time** - when your compiler builds smart-contract code BOC, after FunC code is processed. Fift can look differently:

```
// tuple primitives
x{6F0} @Defop(4u) TUPLE
x{6F00} @Defop NIL
x{6F01} @Defop SINGLE
x{6F02} dup @Defop PAIR @Defop CONS
```
> TVM opcode definitions in Asm.fif

```
"Asm.fif" include
<{ SETCP0 DUP IFNOTRET // return if recv_internal
   DUP 85143 INT EQUAL OVER 78748 INT EQUAL OR IFJMP:<{ // "seqno" and "get_public_key" get-methods
     1 INT AND c4 PUSHCTR CTOS 32 LDU 32 LDU NIP 256 PLDU CONDSEL  // cnt or pubk
   }>
   INC 32 THROWIF	// fail unless recv_external
   9 PUSHPOW2 LDSLICEX DUP 32 LDU 32 LDU 32 LDU 	//  signature in_msg subwallet_id valid_until msg_seqno cs
   NOW s1 s3 XCHG LEQ 35 THROWIF	//  signature in_msg subwallet_id cs msg_seqno
   c4 PUSH CTOS 32 LDU 32 LDU 256 LDU ENDS	//  signature in_msg subwallet_id cs msg_seqno stored_seqno stored_subwallet public_key
   s3 s2 XCPU EQUAL 33 THROWIFNOT	//  signature in_msg subwallet_id cs public_key stored_seqno stored_subwallet
   s4 s4 XCPU EQUAL 34 THROWIFNOT	//  signature in_msg stored_subwallet cs public_key stored_seqno
   s0 s4 XCHG HASHSU	//  signature stored_seqno stored_subwallet cs public_key msg_hash
   s0 s5 s5 XC2PU	//  public_key stored_seqno stored_subwallet cs msg_hash signature public_key
   CHKSIGNU 35 THROWIFNOT	//  public_key stored_seqno stored_subwallet cs
   ACCEPT
   WHILE:<{
     DUP SREFS	//  public_key stored_seqno stored_subwallet cs _51
   }>DO<{	//  public_key stored_seqno stored_subwallet cs
     8 LDU LDREF s0 s2 XCHG	//  public_key stored_seqno stored_subwallet cs _56 mode
     SENDRAWMSG
   }>	//  public_key stored_seqno stored_subwallet cs
   ENDS SWAP INC	//  public_key stored_subwallet seqno'
   NEWC 32 STU 32 STU 256 STU ENDC c4 POP
}>c
```
> wallet_v3_r2.fif

Last fragment of code looks like TVM assembly, and most of it really is! How can this happen?

Imagine you're talking to a trainee programmer, saying him "and now add commands doing this, this and that to the end of function". Your commands end up being in trainee's program. They're processed twice - just like here, opcodes in capital letters (SETCP0, DUP, etc) are processed both by Fift and by TVM.

You can explain high-level abstractions to your trainee, eventually he will understand and be able to use them. Fift is also extensible - you're able to define your own commands. In fact, Asm[Tests].fif is all about defining TVM opcodes.

TVM opcodes, on the other hand, are executed **at run-time** - they're code of smart contracts. They can be thought of as program of your trainee - TVM assembly can do less things (e.g. it doesn't have builtin primitives for signing data - because everything that TVM does in blockchain is public), but it can really interact with its environment.

## Usage in smart-contracts

### [Fift] - Putting big BOC into contract

This is possible if you are using `toncli`. If you use other compilers to build contract, possibly there are other ways to include big BOC.
Edit `project.yaml` so that `fift/blob.fif` is included when building smart-contract code:
```
contract:
  fift:
    - fift/blob.fif
  func:
    - func/code.fc
```

Put the BOC in `fift/blob.boc`, then add the following code to `fift/blob.fif`:
```
<b 8 4 u, 8 4 u, "fift/blob.boc" file>B B>boc ref, b> <s @Defop LDBLOB
```

Now, you're able to extract this blob from smart contract:
```
cell load_blob() asm "LDBLOB";

() recv_internal() {
    send_raw_message(load_blob(), 160);
}
```

### [TVM assembly] - Converting integer to string

"Sadly", int-to-string conversion attempt using Fift primitives fails.
```
slice int_to_string(int x) asm "(.) $>s PUSHSLICE";
```
The reason is obvious: Fift is doing calculations in compile-time, where no `x` is yet available for conversion. To convert non-constant integer to string slice, you need TVM assembly. For example, this is code by one of TON Smart Challenge 3 participants':
```
tuple digitize_number(int value)
  asm "NIL WHILE:<{ OVER }>DO<{ SWAP TEN DIVMOD s1 s2 XCHG TPUSH }> NIP";

builder store_number(builder msg, tuple t)
  asm "WHILE:<{ DUP TLEN }>DO<{ TPOP 48 ADDCONST ROT 8 STU SWAP }> DROP";

builder store_signed(builder msg, int v) inline_ref {
  if (v < 0) {
    return msg.store_uint(45, 8).store_number(digitize_number(- v));
  } elseif (v == 0) {
    return msg.store_uint(48, 8);
  } else {
    return msg.store_number(digitize_number(v));
  }
}
```

### [TVM assembly] - Cheap modulo multiplication

```
int mul_mod(int a, int b, int m) inline_ref {               ;; 1232 gas units
  (_, int r) = muldivmod(a % m, b % m, m);
  return r;
}
int mul_mod_better(int a, int b, int m) inline_ref {        ;; 1110 gas units
  (_, int r) = muldivmod(a, b, m);
  return r;
}
int mul_mod_best(int a, int b, int m) asm "x{A988} s,";     ;; 65 gas units
```

`x{A988}` is opcode formatted according to [5.2 Division](/learn/tvm-instructions/instructions#52-division): division with pre-multiplication, where the only returned result is remainder modulo third argument. But opcode needs to get into smart-contract code - that's what `s,` does: it stores slice on top of stack into builder slightly below.
