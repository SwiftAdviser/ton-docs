# Persistent States
Nodes store snapshots of states of the blockchain periodically. Each state is created at some masterchain block and has some TTL. The block and TTL are chosen using the following algorithm:

Only key blocks can be chosen. A block has some timestamp `ts`. There are periods of time of length `2^17` seconds (approximately up to 1.5 days). The period of a block with timestamp `ts` is `x = floor(ts / 2^17)`. The first key block from each period is chosen to create a persistent state.

TTL of a state from period `x` is equal to `2^(18 + ctz(x))`, where `ctz(x)` is the number of trailing zeroes in the binary representation of `x` (i.e. the largest `y` such that `x` is divisible by `2^y`).

That means that persistent states are created every 1.5 days, half of them have TTL of `2^18` seconds (3 days), half of the remaining states have TTL of `2^19` seconds (6 days) and so on.

In 2022 there is the following long-term (at least 3 months) persistent states (times in the future are approximate):

| Block seqno | Block time | TTL | Expires at |
|--:|--:|--:|--:|
| 18155329 | 2022-02-07 01:31:53 | 777 days | 2024-03-24 18:52:57 |
| 19365422 | 2022-03-27 14:36:58 |  97 days | 2022-07-02 16:47:06 |
| | 2022-05-14 20:00:00 | 194 days | 2022-11-24 23:00:00 |
| | 2022-07-02 09:00:00 |  97 days | 2022-10-07 10:00:00 |
| | 2022-08-19 22:00:00 | 388 days | 2023-09-12 06:00:00 |
| | 2022-10-07 11:00:00 |  97 days | 2023-01-12 12:00:00 |
| | 2022-11-25 00:00:00 | 194 days | 2023-06-07 03:00:00 |
| | 2022-11-25 00:00:00 | 194 days | 2023-06-07 03:00:00 |
| 27747086 | 2022-03-02 05:08:11 | 1553 days | 2027-06-02 18:50:19 |

When the node starts for the first time, it has to download a persistent state. This is implemented in [validator/manager-init.cpp](https://github.com/ton-blockchain/ton/blob/master/validator/manager-init.cpp).

Starting from the init block, the node downloads all newer key blocks. It selects the most recent key block with a persistent state which still exists (using the formula above), and then downloads the corresponding masterchain state and states for all shards (or only the shards that are required for this node).
