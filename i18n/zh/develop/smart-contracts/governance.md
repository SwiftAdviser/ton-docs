# Governance contracts

In TON, consensus parameters of node operation related to TVM, catchain, fees, and chain topology (as well as how those parameters are stored and updated) are controlled by a set of special smart contracts (in contrast to the old-fashioned and inflexible ways of hardcoding those parameters adopted by blockchains of previous generations). That way, TON implements comprehensive and transparent on-chain governance. The set of special contracts itself is governed by parameters and currently includes the Elector, Config, and DNS contracts and in future will be extended by extra-currency Minter and others.

## Elector

The Elector smart contract controls the way how rounds of validation change each other, who gets the duty to validate the blockchain, and how rewards for validation would be distributed. If you want to become a validator and interact with Elector, check [validator instrucitons](https://ton.org/validator).

Elector stores data of Toncoin that is not withdrawn in `credits` hashmap, new applications in `elect` hashmap, and information about previous elections in _past\_elections_ hashmap (the latter is stored inside _complaints_ about validator misbehavior and _frozen_-stakes of validator for already finished rounds, which are withheld for `stake_held_for`(ConfigParam 15)). The Elector contract has three purposes:
 - Process applications for the election of validators
 - Hold elections
 - Process validator misbehaving reports
 - Distribute validation rewards

### Processing applications
To create an application, a future validator needs to form a special message that contains the corresponding parameters (ADNL address, public key, `max_factor`, etc.), attach it to some sum of TON (called a stake), and send it to the Elector. In turn, the Elector checks those parameters and either registers an application or immediately returns the stake back to the sender. Note that applications are only accepted from addresses on the masterchain.

### Conducting elections
The Elector is a special smart contract that has the option to be forcedly invoked at the beginning and end of each block (so-called Tick and Tock transactions). The Elector, indeed, is invoked on each block and checks whether it is time to conduct a new election.

The general concept of the election process is to consider all applications, in particular their TON amount and `max_factor` (the maximal ratio of validation work this applicant is agreed to do in comparison to the weakest validator), and set weights to each validator proportional to the TON amount but in such a way that all `max_factor` conditions are met.

It is technically implemented as follows:

1. Elector takes all applications with a stake amount above the current network minimum `min_stake` (ConfigParam 17).
2. It sorts them by stake in descending order.
3. If there are more participants than the maximum number of validators (`max_validators` ConfigParam 16), discard the tail of the list.
4. Cycle `i` from `1` to `N` (remaining number of participants).
  - Take the first `i` element from the list (sorted in descending order)
  - Assume that _i_-th candidate will be the last accepted (and thus has the lowest weight) and calculate an effective stake (`true_stake` in code) with respect to `max_factor`. In other words, the effective stake of a _j_-th (`j<i`) applicant is calculated as `min(stake[i]*max_factor[j], stake[j])`.
  - Calculate the total effective stake (TES) of participants from 1 to _i_-th. If this TES is higher than the previous known maximal TES, consider it the current best weight configuration.
5. Get the current best configuration, i.e., the weight configuration that utilizes the maximal stake, and send it to the configuration contract (Config contract, see below) to be a new validator set.
6. Put all unused stakes, such as those from applicants that do not become validators and excesses (if any) `stake[j]-min(stake[i]*max_factor[j], stake[j])` to the `credits` table from where they can be requested by applicants.

That way, if we have nine candidates with 100,000 and a factor of 2.7 and one participant with 10,000. The last participant will not be elected: Without him, an effective stake would be 900,000, and with him, only 9 * 27,000 + 10,000 = 253,000. In contrast, if we have one candidate with 100,000 and a factor of 2.7 and nine participants with 10,000, they all become validators. However, the first candidate will only stake 10*2.7 = 27,000 TON with the excess of 73,000 TON going into `credits`.

Note that there are some limitations (obviously controlled by TON configuration parameters) on the resulting validation set, in particular `min_validators`, `max_validators` (ConfigParam 16), `min_stake`, `max_stake`, `min_total_stake`, `max_stake_factor` (ConfigParam 17). If there is no way to meet those conditions with the current applications, elections will be postponed.

### Process of reporting validator misbehavior

Each validator, from time to time, is randomly assigned to create a new block (if the validator fails after a few seconds, this duty is passed to the next validator). The frequency of such assignments is determined by the validator's weight. So, anyone can get the blocks from the previous validation round and check whether the expected number of generated blocks is close to the real number of blocks. A statistically significant deviation (when the number of generated blocks is less than expected) means that a validator is misbehaving. On TON, it is relatively easy to prove misbehavior using Merkle proofs. The Elector contract accepts such proof with a suggested fine from anyone who is ready to pay for its storage and registers the complaint. Then, every validator of the current round checks the complaint, and if it is correct and the suggested fine corresponds to the severity of the misbehavior, they vote for it. Upon getting more than 2/3 of the votes with respect to the weight, the complaint gets accepted, and the fine is withheld from the `frozen` hashmap of the corresponding element of `past_elections`.

### Distribution of validation rewards
The same way as with checking whether it is time to conduct new elections, the Elector in each block checks whether it is time to release funds from `frozen` for stored `past_elections`. At the corresponding block, the Elector distributes accumulated earnings from corresponding validation rounds (gas fees and block creation rewards) to validators of that round proportional to validator weights. After that, stakes with rewards are added to the `credits` table, and the election gets removed from `past_elections` table.


## Config
Config smart contract controls TON configuration parameters. Its logic determines who and under what conditions has permission to change some of those parameters. It also implements a proposal/voting mechanism and validator set rolling updates.

### Validator set rolling updates
Once the Config contract gets a special message from the Elector contract that notifies it of a new validator set being elected, Config puts a new validator set to ConfigParam 36 (next validators). Then, in each block during TickTock transactions, Config checks whether it is time to apply a new validator set (the time `utime_since` is embedded in the validator set itself) and moves the previous set from ConfigParam 34 (current validators) to ConfigParam32 (previous validators) and sets from ConfigParam 36 to ConfigParam 34.

### Proposal/voting mechanism
Anyone who is ready to pay the storage fee for storing the proposal may propose a change of one or more configuration parameters by sending corresponding messages to the Config contract. In turn, any validator in the current set may vote for this proposal by signing an approval message with their private key (note that the corresponding public key is stored in ConfigParam 34). On gaining or not gaining 3/4 of the votes (with respect to validators' weight), the proposal wins or loses the round. Upon winning a critical number of rounds (`min_wins` ConfigParam 11), the proposal is accepted; upon losing a critical number of rounds (`max_losses` ConfigParam 11), it gets discarded.
Note that some of the parameters are considered critical (the set of critical parameters is itself a configuration parameter ConfigParam 10) and, thus require more rounds to be accepted.

Configuration parameter indexes `-999`, `-1000`, `-1001` are reserved for voting for an emergency update mechanism and updating the code of Config and the Elector. When the proposal with the corresponding indexes gains enough votes in enough rounds corresponding to the emergency key, the code of the Config contract or the code of the Elector contract gets updated.


#### Emergency update
Validators may vote to assign a special public key to be able to update configuration parameters when it cannot be done via the voting mechanism. This is a temporary measure that is necessary during the active development of the network. It is expected that as the network matures, this measure will be phased out. As soon as it’s developed and tested, the key will be transferred to a multisignature solution. And once the network has proven its stability, the emergency mechanism will be completely discarded.

Validators indeed voted to assign that key to TON Foundation in July 2021 (masterchain block `12958364`). Note that such a key can only be used to speed up configuration updates. It has no ability to interfere with the code, storage, and balances of any contract on any chain.

History of emergency updates:
 - On April 17, 2022, the number of applications for the election grew big enough that the election could not be conducted under gas limits at that moment. In particular, elections required more than 10 million of gas, while the block `soft_limit` and `hard_limit` were set to `10m` and `20m`  (ConfigParam 22), `special_gas_limit` and `block_gas_limit` were set to `10m` and `10m`, respectively (ConfigParam 20). That way, new validators cannot be set, and due to reaching the block gas limit, transactions that process internal messages on the masterchain could not be included in the block. In turn, that leads to the inability to vote for configuration updates (it was impossible to win the required number of rounds since the current round was unable to finish). An emergency key was used to update ConfigParam 22 `soft_limit` to 22m and `hard_limit` to 25m (in block `19880281`) and ConfigParam 20 `special_gas_limit` to 20m and `block_gas_limit` to 22m (in block `19880300`). As a result, the election was successfully conducted, the next block consumed `10 001 444` gas. The total postponement of elections was about 6 hours, and the functionality of the base chain was unaffected.
 - On March 2, 2023, the number of applications for the election grew big enough that even `20m` were not enough to conduct election. However, this time masterchain continue to process external messages due to higher `hard_limit`. An emergency key was used to update ConfigParam 20 `special_gas_limit` to 25m and `block_gas_limit` to 27m (in block `27747086`). As a result, the election was successfully conducted in next block. The total postponement of elections was about 6 hours, besides elections, functionality of the both master chain and base chain was unaffected.
