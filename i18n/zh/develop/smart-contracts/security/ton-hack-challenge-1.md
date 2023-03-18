# Drawing conclusions from TON Hack Challenge

The TON Hack Challenge was held on October 23.
There were several smart contracts deployed to the TON mainnet with synthetic security breaches. Every contract had a balance of 3000 or 5000 TON, allowing participant to hack it and get rewards immediately.

Source code and contest rules were hosted on Github [here](https://github.com/ton-blockchain/hack-challenge-1).

## Contracts

### 1. Mutual fund

:::note SECURITY RULE
Always check functions for [`impure`](/develop/func/functions#impure-specifier) modifier.
:::

The first task was very simple. The attacker could find that `authorize` function was not `impure`. The absence of this modifier allows a compiler to skip calls to that function if it returns nothing or the return value is unused.

```func
() authorize (sender) inline {
  throw_unless(187, equal_slice_bits(sender, addr1) | equal_slice_bits(sender, addr2));
}
```

### 2. Bank

:::note SECURITY RULE
Always check for [modifying/non-modifying](/develop/func/statements#methods-calls) methods.
:::

`udict_delete_get?` was called with `.` instead `~`, so the real dict was untouched.

```func
(_, slice old_balance_slice, int found?) = accounts.udict_delete_get?(256, sender);
```

### 3. DAO

:::note SECURITY RULE
Use signed integers if you really need it.
:::

Voting power was stored in message as an integer. So the attacker could send a negative value during power transfer and get infinite voting power.

```func
(cell,()) transfer_voting_power (cell votes, slice from, slice to, int amount) impure {
  int from_votes = get_voting_power(votes, from);
  int to_votes = get_voting_power(votes, to);

  from_votes -= amount;
  to_votes += amount;

  ;; No need to check that result from_votes is positive: set_voting_power will throw for negative votes
  ;; throw_unless(998, from_votes > 0);

  votes~set_voting_power(from, from_votes);
  votes~set_voting_power(to, to_votes);
  return (votes,());
}
```

### 4. Lottery

:::note SECURITY RULE
Always randomize seed before doing [`rand()`](/develop/func/stdlib#rand)
:::

Seed was brought from logical time of the transaction, and a hacker can win by bruteforcing the logical time in the current block (cause lt is sequential in the borders of one block).

```func
int seed = cur_lt();
int seed_size = min(in_msg_body.slice_bits(), 128);

if(in_msg_body.slice_bits() > 0) {
    seed += in_msg_body~load_uint(seed_size);
}
set_seed(seed);
var balance = get_balance().pair_first();
if(balance > 5000 * 1000000000) {
    ;; forbid too large jackpot
    raw_reserve( balance - 5000 * 1000000000, 0);
}
if(rand(10000) == 7777) { ...send reward... }
```

### 5. Wallet

:::note SECURITY RULE
Remember that everything is stored in the blockchain.
:::

The wallet was protected with password, it's hash was stored in contract data. However, the blockchain remembers everything—the password was in the transaction history.

### 6. Vault

:::note SECURITY RULE
Always check for [bounced](/develop/smart-contracts/guidelines/non-bouncable-messages) messages.
Don't forget about errors caused by [standard](/develop/func/stdlib/) functions.
Make your conditions as strict as possible.
:::

The vault has the following code in the database message handler:

```func
int mode = null();
if (op == op_not_winner) {
    mode = 64; ;; Refund remaining check-TONs
               ;; addr_hash corresponds to check requester
} else {
     mode = 128; ;; Award the prize
                 ;; addr_hash corresponds to the withdrawal address from the winning entry
}
```

Vault does not have a bounce handler or proxy message to the database if the user sends “check”. In the database we can set `msg_addr_none` as an award address because `load_msg_address` allows it. We are requesting a check from the vault, database tries to parse `msg_addr_none` using [`parse_std_addr`](/develop/func/stdlib#parse_std_addr), and fails. Message bounces to the vault from the database and op is not `op_not_winner`.

### 7. Better bank

:::note SECURITY RULE
Never destroy account for fun.
Make [`raw_reserve`](/develop/func/stdlib#raw_reserve) instead of sending money to yourself.
Think about possible race conditions.
Be careful with hashmap gas consumption.
:::

There were race conditions in the contract: you could deposit money, then try to withdraw it twice in concurrent messages. There is no guarantee that a message with reserved money will be processed, so the bank can shut down after a second withdrawal. After that, the contract could be redeployed and anybody could withdraw unclaimed money.

### 8. Dehasher

:::note SECURITY RULE
Avoid executing third-party code in your contract.
:::

```func
slice try_execute(int image, (int -> slice) dehasher) asm "<{ TRY:<{ EXECUTE DEPTH 2 THROWIFNOT }>CATCH<{ 2DROP NULL }> }>CONT"   "2 1 CALLXARGS";

slice safe_execute(int image, (int -> slice) dehasher) inline {
  cell c4 = get_data();

  slice preimage = try_execute(image, dehasher);

  ;; restore c4 if dehasher spoiled it
  set_data(c4);
  ;; clean actions if dehasher spoiled them
  set_c5(begin_cell().end_cell());

  return preimage;
}
```

There is no way to safe execute a third-party code in the contract, because [`out of gas`](/learn/tvm-instructions/tvm-exit-codes#standard-exit-codes) exception cannot be handled by `CATCH`. The attacker simply can [`COMMIT`](/learn/tvm-instructions/instructions#11-application-specific-primitives) any state of contract and raise `out of gas`.

## Conclusion

Hope this article has shed some light on the non-obvious rules for FunC developers.

## References

Originally written by Dan Volkov

- [dvlkv on Github](https://github.com/dvlkv)
- [Original article](https://dev.to/dvlkv/drawing-conclusions-from-ton-hack-challenge-1aep)
