# TVM Exit codes

If TVM exits with an arbitrary 16-bit unsigned integer `exit_code`. `exit_code` higher than 1, it is considered to be an _error code_, therefore an exit with such a code may cause the transaction to revert/bounce.

## Standard exit codes
* `0` - Standard successful execution exit code.
* `1` - Alternative successful execution exit code.
* `2` - Stack underflow. Last op-code consumed more elements than there are on the stacks. <sup>1</sup>
* `3` - Stack overflow. More values have been stored on a stack than
allowed by this version of TVM.
* `4` - Integer overflow. Integer does not fit into −2<sup>256</sup> ≤ x < 2<sup>256</sup> or a division by zero has occurred.
* `5` - Integer out of expected range.
* `6` - Invalid opcode. Instruction is unknown in the current TVM version.
* `7` - Type check error. An argument to a primitive is of an incorrect value type. <sup>1</sup>
* `8` - Cell overflow. Writing to builder is not possible since after operation there would be more than 1023 bits or 4 references.
* `9` - Cell underflow. Read from slice primitive tried to read more bits or references than there are.
* `10` - Dictionary error. Error during manipulation with dictionary (hashmaps).
* `13` - Out of gas error. Thrown by TVM when the remaining gas becomes negative.
* `32` - Action list is invalid. Set during action phase if c5 register after execution contains unparsable object.
* `32` (the same as prev) - Method ID not found. Returned by TonLib during an attempt to execute non-existent get method.
* `34` - Action is invalid or not supported. Set during action phase if current action cannot be applied.
* `37` - Not enough TON. Message sends too much TON (or there is not enough TON after deducting fees).
* `38` - Not enough extra-currencies.
* `-14` - It means out of gas error, same as `13`. Negative, because it [cannot be faked](https://github.com/ton-blockchain/ton/blob/20758d6bdd0c1327091287e8a620f660d1a9f4da/crypto/vm/vm.cpp#L492)

<sup>1</sup> If you encounter such exception in a _func_ contract it probably means a type error in `asm` declarations.
