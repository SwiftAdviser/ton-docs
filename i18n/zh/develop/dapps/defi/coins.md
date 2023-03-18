# Native token: Toncoin

The native cryptocurrency of the TON Blockchain is **Toncoin**.

Transaction fees, gas payments (i.e., smart contract message processing fees), and persistent storage payments are collected in Toncoin.

Toncoin is used to make the deposits required to become a blockchain validator.

The process of making Toncoin payments is described in the [corresponding section](/develop/dapps/asset-processing).

You can find out where to buy or exchange Toncoin on the [website](https://ton.org/coin).

## Extra currencies

The TON Blockchain supports up to 2^32 built-in extra currencies. 

Extra currency balances can be stored on each blockchain account and transferred to other accounts natively (in an internal message from one smart contract to another, you can specify a hashmap of the extra currency amounts in addition to the Toncoin amount).

TLB: `extra_currencies$_ dict:(HashmapE 32 (VarUInteger 32)) = ExtraCurrencyCollection;` - hashmap of currency ID and amount.

However, extra currencies can only be stored and transferred (like Toncoin) and do not have their own arbitrary code or functionality.

Note that if there are a large number of extra currencies created, the accounts will "swell" because they need to store them.

Thus, extra currencies are best used for well-known decentralized currencies (for example, Wrapped Bitcoin or Ether), and creating such an extra currency should be quite expensive.

[Jettons](/develop/dapps/defi/tokens#jettons) are suitable for other tasks.

At the moment, no extra currency has been created on the TON Blockchain. The TON Blockchain has full support for extra currencies by accounts and messages, but the minter system contract for their creation has not yet been created. 