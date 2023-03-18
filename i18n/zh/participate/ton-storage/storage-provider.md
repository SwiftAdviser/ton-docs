
# Storage provider
*A storage provider* is a service that stores files for a fee. 

## Binaries

You can download `storage-daemon` and `storage-daemon-cli` for Linux/Windows/MacOS binaries from [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest).

## Compile from sources

You can compile `storage-daemon` and `storage-damon-cli` from sources using this [instruction](/develop/howto/compile#storage-daemon).

## Key concepts
It consists of a smart contract that accepts storage requests and manages payment from clients, and an application that uploads and serves the files to clients. Here's how it works:

1. The owner of the provider launches the `storage-daemon`, deploys the main smart contract, and sets up the parameters. The contract's address is shared with potential clients.
2. Using the `storage-daemon`, the client creates a Bag from their files and sends a special internal message to the provider's smart contract.
3. The provider's smart contract creates a storage contract to handle this specific Bag.
4. The provider, upon finding the request in the blockchain, downloads the Bag and activates the storage contract.
5. The client can then transfer payment for storage to the storage contract. To receive the payment, the provider regularly presents the contract with proof that they are still storing the Bag.
6. If the funds on the storage contract run out, the contract is considered inactive and the provider is no longer required to store the Bag. The client can either refill the contract or retrieve their files.

:::info
The client can also retrieve their files at any time by providing proof of ownership to the storage contract. The contract will then release the files to the client and deactivate itself.
:::

## Smart contract

[Smart Contract Source Code](https://github.com/ton-blockchain/ton/tree/master/storage/storage-daemon/smartcont).

## Using a Provider by Clients
In order to use a storage provider, you need to know the address of its smart contract. The client can obtain the provider's parameters with the following command in `storage-daemon-cli`:
```
get-provider-params <address>
```

### The provider's parameters:

* Whether new storage contracts are accepted.
* Minimum and maximum *Bag* size (in bytes).
* Rate - the cost of storage. Specified in nanoTON per megabyte per day.
* Max span - how often the provider should provide proofs of *Bag* storage.

### A request to store

You need to create a *Bag* and generate a message with the following command:

```
new-contract-message <BagID> <file> --query-id 0 --provider <address>
```

### Info:

Executing this command may take some time for large *Bags*. The message body will be saved to `<file>` (not the entire internal message). Query id can be any number from 0 to `2^64-1`. The message contains the provider's parameters (rate and max span). These parameters will be printed out after executing the command, so they should be double checked before sending. If the provider's owner changes the parameters, the message will be rejected, so the conditions of the new storage contract will be exactly what the client expects.

The client must then send the message with this body to the provider's address. In case of an error the message will come back to the sender (bounce). Otherwise, a new storage contract will be created and the client will receive a message from it with [`op=0xbf7bd0c1`](https://github.com/ton-blockchain/ton/tree/testnet/storage/storage-daemon/smartcont/constants.fc#L3) and the same query id.

At this point the contract is not yet active. Once the provider downloads the *Bag*, it will activate the storage contract and the client will receive a message with [`op=0xd4caedcd`](https://github.com/SpyCheese/ton/blob/tonstorage/storage/storage-daemon/smartcont/constants.fc#L4) (also from the storage contract).

The storage contract has a "client balance" - these are the funds that the client transferred to the contract and which have not yet been paid to the provider. Funds are gradually debited from this balance (at a rate equal to the rate per megabyte per day). The initial balance is what the client transferred with the request to create the storage contract. The client can then top up the balance by making simple transfers to the storage contract (this can be done from any address). The remaining client balance is returned by the [`get_storage_contract_data`](https://github.com/ton-blockchain/ton/tree/testnet/storage/storage-daemon/smartcont/storage-contract.fc#L222) get method as the second value (`balance`).

### The contract may be closed for the following cases:

:::info
In case of the storage contract being closed, the client receives a message with the remaining balance and [`op=0xb6236d63`](https://github.com/ton-blockchain/ton/tree/testnet/storage/storage-daemon/smartcont/constants.fc#L6). 
:::

* Immediately after creation, before activation, if the provider refuses to accept the contract (the provider's limit is exceeded or other errors).
* The client balance reaches 0.
* The provider can voluntarily close the contract.
* The client can voluntarily close the contract by sending a message with [`op=0x79f937ea`](https://github.com/ton-blockchain/ton/tree/testnet/storage/storage-daemon/smartcont/constants.fc#L2) from its own address and any query id.


## Running and Configuring a Provider
The Storage Provider is part of the `storage-daemon`, and is managed by the `storage-daemon-cli`. `storage-daemon` needs to be started with the `-P` flag.


### Create a main smart contract

You can do this from `storage-daemon-cli`:
```
deploy-provider
```

:::info IMPORTANT!
You will be asked to send a non-bounceable message with 1 TON to the specified address in order to initialize the provider. You can check that the contract has been created using the `get-provider-info` command.
:::

By default, the contract is set to not accept new storage contracts. Before activating it, you need to configure the provider. The provider's settings consist of a configuration (stored in `storage-daemon`) and contract parameters (stored in the blockchain).

### Configuration:
* `max contracts` - maximum number of storage contracts that can exist at the same time.
* `max total size` - maximum total size of *Bags* in storage contracts.
You can view the configuration values using `get-provider-info`, and change them with:
```
set-provider-config --max-contracts 100 --max-total-size 100000000000
```

### Contract parameters:
* `accept` - whether to accept new storage contracts.
* `max file size`, `min file size` - size limits for one *Bag*.
* `rate` - storage cost (specified in nanoTONs per megabyte per day).
* `max span` - how often the provider will have to submit storage proofs.

You can view the parameters using `get-provider-info`, and change them with:
```
set-provider-params --accept 1 --rate 1000000000 --max-span 86400 --min-file-size 1024 --max-file-size 1000000000
```

### It is worth paying attention

Note: in the `set-provider-params` command, you can specify only some of the parameters. The others will be taken from the current parameters. Since the data in the blockchain is not updated instantly, several consecutive `set-provider-params` commands can lead to unexpected results.

It is recommended to initially put more than 1 TON on the provider's balance, so that there are enough funds to cover the commissions for working with storage contracts. However, do not send too many TONs with the first non-bounceable message.

After setting the `accept` parameter to `1`, the smart contract will start accepting requests from clients and creating storage contracts, while the storage daemon will automatically process them: downloading and distributing *Bags*, generating storage proofs.


## Further Work With the Provider

### List of existing storage contracts

```
get-provider-info --contracts --balances
```
Each storage contract has a `Client$` and `Contract$` balance listed; the difference between them can be withdrawn to the main provider contract with the command `withdraw <address>`.

The command `withdraw-all` will withdraw funds from all contracts that have at least `1 TON` available.

Any storage contract can be closed with the command `close-contract <address>`. This will also transfer the funds to the main contract. The same will happen automatically when the client's balance runs out. The *Bag* files will be deleted in this case (unless there are other contracts using the same *Bag*).

### Transfer

You can transfer funds from the main smart contract to any address (the amount is specified in nanoTON):
```
send-coins <address> <amount>
send-coins <address> <amount> --message "Some message"
```

:::info
All *Bags* stored by the provider are available with the command `list`, and can be used as usual. To prevent disrupting the provider's operations, do not delete them or use this storage daemon to work with any other *Bags*.
:::
