# Random number generation

Generating random numbers is a common task which you may need in many different projects. You might have already seen `random()` function in FunC docs, but note that its result can be easily predicted unless you use some additional tricks.

## How can someone predict a random number?

Computers are terrible at generating random information, because all they do is following the instructions of users. But since people really need random numbers often, they came up with different ways of generating _pseudo-random_ numbers.

These algorithms usually require you to provide some _seed_ value which will be used to generate a sequence of pseudo-random numbers. So if you run the same program with the same _seed_ several times, you will eventually get the same result every time. In TON, the _seed_ is different for each block.

 * [Generation of block random seed](https://ton.org/docs/participate/own-blockchain-software/random)

So in order to predict the result of `random()` function in some smart contract, you just need to know the current _seed_ of the block (which is possible).

## And what about `randomize_lt()`?

To make the random number generation a bit more unpredictable, you can add the current `Logical time` to the _seed_, so different transactions will have different `seeds` and different results. But the thing is that `Logical time` is easily predictable.

As was seen in TON Hack Challenge, generating random numbers with just `randomize_lt()` and `random()` is not safe. Take a look at the solution of 4th task called **Lottery**:
 - [Original solution of the 4th task](https://github.com/ton-blockchain/hack-challenge-1/blob/master/Solutions/4.%20lottery.md)
 - [Drawing conclusions from TON Hack Challenge \(Task 4\)](/develop/smart-contracts/security/ton-hack-challenge-1#4-lottery)

You can predict the results of `random()` by writing a simple smart contract function even if there was a `randomize_lt()` call.

## So, how do I generate random numbers safely?

There can be different approaches, but the simpliest one is just mixing several parameters to _seed_. This can be easily done like this:
```func
int seed = cell_hash(begin_cell()
    .store_uint(now(), 256)
    .store_uint(block_lt(), 256)
    .store_uint(cur_lt(), 256)
.end_cell());
randomize(seed);
;; now you can just call rand() or random() functions to get random numbers
```

This is enough for most cases, but there is still a chance that some evil validator will specifically substitute parameters like the current time to get such a _seed_, with which he will get the number he needs.

In order to prevent (or at least complicate) the substitution of the _seed_, you can use more complex schemes. For example, you can skip one block before generating a random number. If we skip a block, the _seed_ will change in a less predictable way, thus your RNG will be a lot safer.

Skipping blocks is not a complex task. You can do that by simply sending a message to Masterchain and back to the workchain of your contract. Let's have a look at the simple example!

:::caution
Do not use this example contract in real projects, write your own instead.
:::

### Masterchain echo-contract

The purpose of this contract is just to forward the message back to the sender. This can be done in a few FunC lines of code:

```func
() recv_internal (cell in_msg_full, slice in_msg_body) impure {
    var cs = in_msg_full.begin_parse();
    var flags = cs~load_uint(4);
    if (flags & 1) { ;; ignore bounced messages
        return ();
    }
    slice sender = cs~load_msg_addr();
    send_raw_message(
        begin_cell()
            .store_uint(0x18, 6)
            .store_slice(sender)
            .store_coins(0)
            .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
            .store_slice(in_msg_body)
        .end_cell(),
        64 + 2 ;; send the remaining value of an incoming msg & ignore errors
    );
}
```

Just deploy this contract in Masterchain and let's move to the main contract.

### Main contract in any workchain

Let's write a simple lottery contract as an example. User will send 1 TON to it and with a chance of 50% will get 2 TON back.

```func
;; set the echo-contract address
const echo_address = "Ef8Nb7157K5bVxNKAvIWreRcF0RcUlzcCA7lwmewWVNtqM3s"a;

() recv_internal (int msg_value, cell in_msg_full, slice in_msg_body) impure {
    var cs = in_msg_full.begin_parse();
    var flags = cs~load_uint(4);
    if (flags & 1) { ;; ignore bounced messages
        return ();
    }
    slice sender = cs~load_msg_addr();

    int op = in_msg_body~load_uint(32);
    if ((op == 0) & equal_slice_bits(in_msg_body, "bet")) { ;; bet from user
        throw_unless(501, msg_value == 1000000000); ;; 1 TON
        
        send_raw_message(
            begin_cell()
                .store_uint(0x18, 6)
                .store_slice(echo_address)
                .store_coins(0)
                .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
                .store_uint(1, 32) ;; let 1 be echo opcode in our contract
                .store_slice(sender) ;; forward user address
            .end_cell(),
            64 ;; send the remaining value of an incoming msg
        );
    }
    elseif (op == 1) { ;; echo
        throw_unless(502, equal_slice_bits(sender, echo_address)); ;; only accept echoes from our echo-contract
        
        slice user = in_msg_body~load_msg_addr();

        {-
            at this point we have skipped 1+ blocks
            so let's just generate the random number
        -}
        randomize_lt();
        int x = rand(2); ;; generate a random number (either 0 or 1)
        if (x == 1) { ;; user won
            send_raw_message(
                begin_cell()
                    .store_uint(0x18, 6)
                    .store_slice(user)
                    .store_coins(2000000000) ;; 2 TON
                    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
                .end_cell(),
                3 ;; ignore errors & pay fees separately
            );
        }
    }
}
```

Deploy this contract in any workchain you need (probably Basechain) and you're done!

## Is this method 100% secure?

It is safe in most cases, but there is still a **chance of manipulating it**.

An evil validator with some probability [can affect](/participate/own-blockchain-software/random#conclusion) the _seed_, on which the random depends. Even if this probability is extremely small, it is still worth considering.