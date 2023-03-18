# "accept_message" effects

`accept_message` and `set_gas_limit` may cause not that straightforward effects when doing exactly what it's said in the [stdlib reference](/develop/func/stdlib#accept_message).

## External messages

External messages are processed as follows: `gas_limit` is set to `gas_credit` (ConfigParam 20 and ConfigParam 21) equal to 10k gas. During the spending of those credits, a contract should call `accept_message` to `set_gas_limit` indicating that it is ready to pay fees for message processing. If `gas_credit` is reached or computation is finished, while `accept_message` is not called, this message will be completely discarded (like it never existed at all). Otherwise, a new gas limit equal to `contract_balance/gas_price` (in case of `accept_message`) or a custom number (in the case of `set_gas_limit`) will be set; after the transaction ends, full computation fees will be deducted from the contract balance (that way `gas_credit` is **credit** indeed, not free gas).

Note that if after `accept_message` some error is thrown (both in ComputePhase or ActionPhase) transaction will be written to the blockchain and fees will be deducted from the contract balance, but storage will not be updated and actions will not be applied as in any transaction with an error exit code. As a result, if the contract accepts an external message and then throws an exception due to an error in the message data or sending an incorrectly serialized message, it will pay for processing but have no way of preventing message replay. The same message will be accepted by contract over and over until it consumes the entire balance.

## Internal message

By default, when contract gets internal message gas limit is set to `message_balance/gas_price`, in other words, message pays for it's processing. By using `accept_message`/`set_gas_limit` contract may change gas limit during execution. Note that manual settings of gas limits do not interfere with bouncing behavior; messages will be bounced if sent in bounceable mode and contain enough money to pay for their processing and creation of bounce messages.

:::info example
For instance, if you send a bounceable message with 0.1 TON in basechain that is accepted by a contract with 1 TON balance, computation costs 0.005 TON, and message fee 0.001 TON, then bounce message will contain `0.1 - 0.005 - 0.001 ` = `0.094` TON.

If in the same example, computation cost will be 0.5 (instead of 0.005), there will be no bounce (message balance should be `0.1 - 0.5 - 0.001 = -0.401`, thus no bounce) and contract balance will be `1 + 0.1 - 0.5` = `0.6` TON
:::
