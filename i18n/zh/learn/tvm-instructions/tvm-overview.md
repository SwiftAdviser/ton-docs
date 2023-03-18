# TVM Overview



All TON Smart Contracts are executed on their own TON Virtual Machine (TVM). TVM is built on the _stack principle_, which makes it efficient and easy to implement.

This document provides a bird's-eye overview of how TVM executes transactions.

:::tip

* There is also a detailed specification — [**Whitepaper**](https://ton.org/tvm.pdf)
* Could be useful — [**TVM C++ implementation**](https://github.com/ton-blockchain/ton/tree/master/crypto/vm)

:::

## Transactions and phases
When some event happens on the account in one of the TON chains, it causes a **transaction**.  The most common event is the "arrival of some message", but generally speaking there could be `tick-tock`, `merge`, `split` and other events.

Each transaction consists of up to 5 phases.
1. **Storage phase** - in this phase, storage fees accrued by the contract due to the occupation of some space in the chain state are calculated. Read more in [Storage Fees](/develop/smart-contracts/fees#storage-fee).
2. **Credit phase** - in this phase, the balance of the contract with respect to a (possible) incoming message value and collected storage fee are calculated
3. **Compute phase** - in this phase, TVM is executed (see below), the result of the TVM execution is an aggregation of `exit_code`, `actions` (serialized list of actions), `gas_details`, `new_storage` and some others.
4. **Action phase** - if the compute phase was successful, in this phase `actions` from the compute phase are processed. In particular, actions may include the sending of messages, updating the smart contract code, updating the libraries etc. Note that some actions may fail during processing (for instance we try to send message with more TON than the contract has), in that case the whole transaction may revert or this action may be skipped (it depends on the mode of the actions, in other words, the contract may send a `send-or-revert` or  `try-send-if-no-ignore` type of message).
5. **Bounce phase** - if the compute phase failed (it returned `exit_code >= 2`), in this phase, _bounce message_ is formed for transactions initiated by an incoming message.

## Compute phase
In this phase, the TVM execution occurs.

### TVM state
At any one moment, the TVM state is fully determined by 6 properties:
* Stack (see below)
* Control registers - (see below) to put it simply, this means up to 16 variables which may be directly set and read during execution
* Current continuation - object which describes a sequence of instructions which is currently executed
* Current codepage - to put it simply, this means the version of TVM which is currently running
* Gas limits - a set of 4 integer values; the current gas limit g<sub>l</sub>, the maximal gas limit g<sub>m</sub>, the remaining gas g<sub>r</sub> and the gas credit g<sub>c</sub>
* Library context - the hashmap of libraries which can be called by TVM 

### TVM is a stack machine
TVM is a last-input-first-output stack machine. There are 7 types of variables which may be stored in stack:
* Integer - signed 257-bit integers
* Tuple - ordered collection of up to 255 elements having arbitrary value types, possibly distinct.
* Null

And four distinct flavours of cells:
* Cell - basic (possibly nested) opaque structure used by TON Blockchain for storing all data
* Slice - special object which allows you to read from a cell
* Builder - special object which allows you to create new cells
* Continuation - special object which allows you to use a cell as source of TVM instructions

### Control registers
* `c0` — Contains the next continuation or return continuation (similar to the subroutine return address in conventional designs). This value must be a Continuation.
* `c1` — Contains the alternative (return) continuation; this value must be a Continuation. 
* `c2` — Contains the exception handler. This value is a Continuation, invoked whenever an exception is triggered.
* `c3` — Supporting register, contains the current dictionary, essentially a hashmap containing the code of all functions used in the program. This value must be a Continuation. 
* `c4` — Contains the root of persistent data, or simply the `data` section of the contract. This value is a Cell.
* `c5` — Contains the output actions. This value is a Cell.
* `c7` — Contains the root of temporary data. It is a Tuple.

### Initialization of TVM
So when a transaction execution gets to the Computation phase, TVM initialises and then executes commands (opcodes) from _Current continuation_ until there are no more commands to execute (and no continuation for return jumps).

A detailed description of initialization can be found in [TON Blockchain 4.4](https://ton.org/tblkch.pdf).
For ordinary transactions caused by message the initial state is as follows:
* stack: 5 elements are put to the stack
    * The balance of the smart contract (after crediting the value of the inbound message) is passed as an Integer amount of nanotons.
    * The balance of inbound message `m` is passed as an Integer amount of nanotons.
    * The inbound message is passed as a cell, which contains a serialized value of type Message X, where X is the type of the message body.
    * The body of the inbound message, equal to the value of field body of `m`, is passed as a cell slice
    * The function selector `s`, an Integer: `0` for tx caused by internal messages, `-1` for external, etc. Generally speaking it is the integer that identifies which event caused the transaction
 * Current continuation: continuation converted from the `code` section of the smart contract
 * Registers initialize as follows: c0, c1, c2 and c3 are empty. c4 contains the cell from the `data` section of the smart contract. c5 contains an empty list (it is serialized as a cell which contain last action in list plus reference to prev one) of output actions. c7 is initialized as tuple with some basic blockchain context data such as time, global config, block_data, etc. See [TON Blockchain 4.4.10](https://ton.org/tblkch.pdf)
 * Current codepage is set to default value (cp=0)
 * Gas limits are initialized in accordance to Credit phase results
 * Library context is initialized as result of merging this smart contract library collection, masterchain global library collection and incoming (if any) message library collection

## TVM instructions

The list of TVM instructions can be found here: [TVM instructions](/learn/tvm-instructions/instructions).

### Result of TVM execution
Besides exit_code and consumed gas data, TVM indirectly outputs the following data:
* c4 register - the cell which will be stored as new `data` of the smart-contract (if execution will not be reverted on this or later phases)
* c5 register - (list of output actions) the cell with last action in the list and reference to the cell with prev action (recursively)

All other register values will be neglected.

Note, that since there is a limitation on max cell-depth `<1024`, and particularly a limitation on c4 and c5 depth `<=512`, there will be a limitation on the number of output actions in one tx `<=255`. If a contract need to send more than that, it may send a message with the request `continue_sending` to itself and send all necessary messages in subsequent transactions.
