# Using toncli

:::tip starter tip
If you didn't use toncli before, try [QUICK START GUIDE](https://github.com/disintar/toncli/blob/master/docs/quick_start_guide.md).
:::

## Testing using toncli

`toncli` uses FunC to test smart contracts. Also, the latest version supports Docker for quick environment setup.

This tutorial will help you test the functions of our smart contract to make sure that the project is working correctly.

The best tutorial describing testing using toncli is:
* [How does the FunC test work?](https://github.com/disintar/toncli/blob/master/docs/advanced/func_tests_new.md)
* [How to debug transactions with toncli?](https://github.com/disintar/toncli/blob/master/docs/advanced/transaction_debug.md)

## FunC test structure under toncli

To test our smart contract, we will have to write 2 functions. One of which takes values, contains the desired result, gives an error if the function under test does not work correctly.

### Let's create a file with tests

Create in the `tests` folder, the file `example.func` in which we will write our tests.

### Data function

As a rule, the testing function does not accept arguments, but must return them.

* **function selector** - id of the called function in the tested contract;
* **tuple** - (stack) values ​​that we will pass to the function that performs tests;
* **c4 cell** - "permanent data" in the control register c4;
* **c7 tuple** - "temporary data" in the control register c7;
* **gas limit integer** - gas limit (to understand the concept of gas, I advise you to first read about it in Ethereum);

:::info About Gas
Gas is a value that shows how many resources a smart contract spends on its execution. Accordingly, the smaller it is, the better.

And you can read in detail [here](https://ton-blockchain.github.io/docs/#/smart-contracts/fees). Well, in full detail here in [Appendix A](https://ton-blockchain.github.io/docs/tvm.pdf).

More about registers c4 and c7 [here](https://ton-blockchain.github.io/docs/tvm.pdf) in 1.3.1
:::

## Let's start writing tests for our smart contract

### Introduction

In the new tests, testing occurs through two functions that allow you to call smart contract methods:

* `invoke_method`, which assumes no exception will be thrown
* `invoke_method_expect_fail`, which assumes an exception will be thrown

These are the functions inside the testing function, which can return any number of values, all of them will be displayed when the tests are run in the report.    

:::info Important!
It is worth noting that each test function name must begin with `_test`.
:::

### Creating a test function

Let's call our test function `__test_example()`, it will return the amount of gas consumed, so it will be `int`.

```js
int __test_example() {

}
```

### Register update c4

Since we will need to frequently update the `c4` register due to a large number of tests, so we will create a helper function that will write `c4` to zero

```js
() set_default_initial_data() impure {
  set_data(begin_cell().store_uint(0, 64).end_cell());
}
```

* `begin_cell()` - will create a Builder for the future cell 
* `store_uint()` - writes the value of total 
* `end_cell()`- create Cell 
* `set_data()` - writes the cell to register c4

`impure` is a keyword that indicates that the function changes the smart contract data.

We got a function that we will use in the body of our testing function

**Result:**

```js
int __test_example() {
	set_default_initial_data();

}
```

### Test Methods

It is worth noting that in the new version of the tests, we have the ability to call several smart contract methods in the testing function.

Inside our test, we will call the `recv_internal()` method and the Get method, so we will increment the value in c4 with the message and immediately check that the value has changed to the one sent.

To call the `recv_internal()` method, we need to create a cell with a message.

```js
int __test_example() {
	set_default_initial_data();
	cell message = begin_cell().store_uint(10, 32).end_cell();
}
```

After this step, we are going to use the `invoke_method` method.

This method takes two arguments:
* method name
* arguments to test as a `tuple`

Two values ​​are returned: the gas used and the values ​​returned by the method (as a tuple).

:::info It's worth noting
Two values ​​are returned: the gas used and the values ​​returned by the method (as a tuple).
:::

In the first call, the arguments will be `recv_internal` and a tuple with a message transformed into a slice using `begin_parse()`

```js 
var (int gas_used1, _) = invoke_method(recv_internal, [message.begin_parse()]);
```

For the record, let's store the amount of gas used in int `gas_used1`.

In the second call, the arguments will be the Get method `get_total()` and an empty tuple.

```js
var (int gas_used2, stack) = invoke_method(get_total, []);
```

For the report, we also store the amount of gas used in `int gas_used2`, plus the values ​​that the method returns, to check later that everything worked correctly.

We get:

```js
int __test_example() {
	set_default_initial_data();

	cell message = begin_cell().store_uint(10, 32).end_cell();
	var (int gas_used1, _) = invoke_method(recv_internal, [message.begin_parse()]);
	var (int gas_used2, stack) = invoke_method(get_total, []);

}
```

Now, finally, the most important step. We have to check if our smart contract is working properly.

That is, if it returns the **correct result**, we return `success` or `failure` and the gas used.

``` js
[int total] = stack; 
throw_if(101, total != 10); 
```
**Explanations:**
* Passing a tuple
* In the first argument, the number of the error (101), which we will receive if the smart contract does not work correctly
* In the second argument is the correct answer

``` js
int __test_example() {
	set_data(begin_cell().store_uint(0, 64).end_cell());
	cell message = begin_cell().store_uint(10, 32).end_cell();
	var (int gas_used1, _) = invoke_method(recv_internal, [message.begin_parse()]);
	var (int gas_used2, stack) = invoke_method(get_total, []);
	[int total] = stack;
	throw_if(101, total != 10);
	return gas_used1 + gas_used2;
}
```

This is the whole test, very convenient.
