# Extra Currency Minting

## Extracurrency
According to [Ton Blockchain Whitepaper 3.1.6](https://ton-blockchain.github.io/docs/tblkch.pdf#page=55), TON Blockchain allows its users to define arbitrary cryptocurrencies or tokens apart from the Toncoin, provided some conditions are met. Such additional cryptocurrencies are identified by 32-bit _currency\_ids_. The list of defined additional cryptocurrencies is a part of the blockchain configuration,
stored in the masterchain. Each internal message as well as account balance contains a special field for `ExtraCurrencyCollection` (set of extracurrencies attached to a message or kept on balance):
```tlb
extra_currencies$_ dict:(HashmapE 32 (VarUInteger 32)) = ExtraCurrencyCollection;
currencies$_ grams:Grams other:ExtraCurrencyCollection = CurrencyCollection;
```

## Extracurrency config
A dictionary, or to be precise `ExtraCurrencyCollection`, of all currencies that should be minted is stored in `ConfigParam7`:
```tlb
_ to_mint:ExtraCurrencyCollection = ConfigParam 7;
```

`ConfigParam 6` contains data related to minting:

```tlb
_ mint_new_price:Grams mint_add_price:Grams = ConfigParam 6;
```

`ConfigParam2` contains address of _Minter_.



## Low-level minting flow
In each block, the collator compares the old global balance (global balance of all currencies at the end of prev block) with `ConfigParam7`. If any amount for any currency in `ConfigParam7` is less than it is in the global balance - the config is invalid. If any amount of any currency in `ConfigParam7` is higher than it is in the global balance a minting message will be created. 

This minting message has source `-1:0000000000000000000000000000000000000000000000000000000000000000` and _Minter_ from `ConfigParam2` as destination and contains excesses of extracurrencies in `ConfigParam7` over old global balance.

The issue here is that the minting message contains extra currencies only and no TON coins. That means that even if _Minter_ is set as a fundamental smart contract (presented in `ConfigParam31`), a minting message will cause the aborted transaction: `compute_ph:(tr_phase_compute_skipped reason:cskip_no_gas)`.

## High-level minting flow
_Minter_ smart contract upon receiving a request for the creation of new extracurrencies or minting additional tokens for existing ones should:
1.  Check that fee determined in `ConfigParam6` can be deducted from the request message
2. 
   1.  for existing tokens: check authorization for minting (only the _owner_ can mint new ones)
   2. for the creation of new currencies: check that id of the cryptocurrency is not occupied and store owner of the new currency
3. send message to config contract (such message should cause the addition to `ExtraCurrencyCollection` in `ConfigParam7`)
4. send message to `0:0000...0000` (which is guaranteed to bounce in the next or following blocks) with extra_currency id

Upon receiving message from `0:0000...0000` 
1. read extra_currency id from the bounce message
2. if there are tokens with corresponding id on minter balance send them to this currency owner with `ok` message
3. otherwise send to currency owner `fail` message

## Issues to be resolved
1. Workaround with sending a message to `0:0000...0000` for postponement of request processing is quite dirty.
2. Cases, when minting failed, should be thought out. For now, it looks like the only possible situation is when a currency amount is 0 or such that the current balance plus a minted amount doesn't fit into `(VarUInteger 32)`
3. How to burn? At first glance, there are no ways.
4. Should minting fees be prohibitive? In other words, is it dangerous to have millions of extracurrencies (big config, potential DoS due to unbound number of dict operations on collation?)


