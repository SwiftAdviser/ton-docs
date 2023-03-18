# 陳述句
本節簡要討論FunC陳述句，它們構成普通函數主體的代碼。

## 表達式陳述句
最常見的一種陳述句是表達式陳述句。它是一個表達式後跟著 `;`。表達式的描述可能會很複雜，因此這裡只呈現一個簡略的概述。通常情況下，所有的子表達式都從左到右計算，但有一個例外是 [asm stack rearrangement](functions#rearranging-stack-entries)，它可以手動定義計算順序。

### 變量聲明
沒有定義其初始值，就無法聲明一個本地變量。

以下是一些變量聲明的示例：

```func
int x = 2;
var x = 2;
(int, int) p = (1, 2);
(int, var) p = (1, 2);
(int, int, int) (x, y, z) = (1, 2, 3);
(int x, int y, int z) = (1, 2, 3);
var (x, y, z) = (1, 2, 3);
(int x = 1, int y = 2, int z = 3);
[int, int, int] [x, y, z] = [1, 2, 3];
[int x, int y, int z] = [1, 2, 3];
var [x, y, z] = [1, 2, 3];
```

在同一範圍內變量可以 "重新聲明"。例如，這是正確的代碼:
```func
int x = 2;
int y = x + 1;
int x = 3;
```
事實上，第二次出現的 `int x` 不是一個聲明，而只是在編譯時保證 `x` 具有類型 `int`。因此，第三行基本上相當於一個簡單的賦值 `x = 3;`。

在嵌套作用域中，一個變量可以像在 C 語言中一樣被真正地重新聲明。例如，考慮以下代碼：

```func
int x = 0;
int i = 0;
while (i < 10) {
  (int, int) x = (i, i + 1);
  ;; here x is a variable of type (int, int)
  i += 1;
}
;; here x is a (different) variable of type int
```
But as mentioned in the global variables [section](/develop/func/global_variables.md), a global variable cannot be redeclared.

Note that a variable declaration **is** an expression statement, so actually constructions like `int x = 2` are full-fledged expressions. For example, this is a correct code:
```func
int y = (int x = 3) + 1;
```
It is a declaration of two variables `x` and `y` equal to `3` and `4` correspondingly.
#### Underscore
Underscore `_` is used when a value is not needed. For example, suppose a function `foo` has type `int -> (int, int, int)`. We can get the first returned value and ignore the second and third like this:
```func
(int fst, _, _) = foo(42);
```
### Function application
A call of a function looks like as such in a conventional language. The arguments of the function call are listed after the function name, separated by commas.
```func
;; suppose foo has type (int, int, int) -> int
int x = foo(1, 2, 3);
```

But notice that `foo` is actually a function of **one** argument of type `(int, int, int)`. To see the difference, suppose `bar` is a function of type `int -> (int, int, int)`. Unlike in conventional languages, you can compose the functions like that:
```func
int x = foo(bar(42));
```
instead of the similar but longer form:
```func
(int a, int b, int c) = bar(42);
int x = foo(a, b, c);
```

Also Haskell-style calls are possible, but not always (to be fixed later):
```func
;; suppose foo has type int -> int -> int -> int
;; i.e. it's carried
(int a, int b, int c) = (1, 2, 3);
int x = foo a b c; ;; ok
;; int y = foo 1 2 3; wouldn't compile
int y = foo (1) (2) (3); ;; ok
```
### Lambda expressions
Lambda expressions are not supported yet.

### Methods calls

#### Non-modifying methods
If a function has at least one argument, it can be called as a non-modifying method. For example, `store_uint` has type `(builder, int, int) -> builder` (the second argument is the value to store, and the third is the bit length). `begin_cell` is a function that creates a new builder. The following codes are equivalent:
```func
builder b = begin_cell();
b = store_uint(b, 239, 8);
```
```func
builder b = begin_cell();
b = b.store_uint(239, 8);
```
So the first argument of a function can be passed to it being located before the function name, if separated by `.`. The code can be further simplified:
```func
builder b = begin_cell().store_uint(239, 8);
```
Multiple calls of methods are also possible:
```func
builder b = begin_cell().store_uint(239, 8)
                        .store_int(-1, 16)
                        .store_uint(0xff, 10);
```
#### Modifying methods
If the first argument of a function has type `A` and the return value of the function has the shape of `(A, B)` where `B` is some arbitrary type, then the function can be called as a modifying method. Modifying method calls may take some arguments and return some values, but they modify their first argument, that is, assign the first component of the returned value to the variable from the first argument. For example, suppose `cs` is a cell slice and `load_uint` has type `(slice, int) -> (slice, int)`: it takes a cell slice and number of bits to load and returns the remainder of the slice and the loaded value. The following codes are equivalent:
```func
(cs, int x) = load_uint(cs, 8);
```
```func
(cs, int x) = cs.load_uint(8);
```
```func
int x = cs~load_uint(8);
```
In some cases we want to use a function as a modifying method that doesn't return any value and only modifies the first argument. It can be done using unit types as follows: Suppose we want to define function `inc` of type `int -> int`, which increments an integer, and use it as a modifying method. Then we should define `inc` as a function of type `int -> (int, ())`:
```func
(int, ()) inc(int x) {
  return (x + 1, ());
}
```
When defined like that, it can be used as a modifying method. The following will increment `x`.
```func
x~inc();
```

#### `.` and `~` in function names
Suppose we want to use `inc` as a non-modifying method too. We can write something like that:
```func
(int y, _) = inc(x);
```
But it is possible to override the definition of `inc` as a modifying method.
```func
int inc(int x) {
  return x + 1;
}
(int, ()) ~inc(int x) {
  return (x + 1, ());
}
```
And then call it like that:
```func
x~inc();
int y = inc(x);
int z = x.inc();
```
The first call will modify x; the second and third won't.

In summary, when a function with the name `foo` is called as a non-modifying or modifying method (i.e. with `.foo` or `~foo` syntax), the FunC compiler uses the definition of `.foo` or `~foo` correspondingly if such a definition is presented, and if not, it uses the definition of `foo`.

### Operators
Note that currently all of the unary and binary operators are integer operators. Logical operators are represented as bitwise integer operators  (cf. [absence of boolean type](/develop/func/types#absence-of-boolean-type)).
#### Unary operators
There are two unary operators:
- `~` is bitwise not (priority 75)
- `-` is integer negation (priority 20)

They should be separated from the argument:
- `- x` is ok.
- `-x` is not ok (it's a single identifier)

#### Binary operators
With priority 30 (left-associative):
- `*` is integer multiplication
- `/` is integer division (floor)
- `~/` is integer division (round)
- `^/` is integer division (ceil)
- `%` is integer reduction by modulo (floor)
- `~%` is integer reduction by modulo (round)
- `^%` is integer reduction by modulo (ceil)
- `/%` returns the quotient and the remainder
- `&` is bitwise AND

With priority 20 (left-associative):
- `+` is integer addition
- `-` is integer subtraction
- `|` is bitwise OR
- `^` is bitwise XOR

With priority 17 (left-associative):
- `<<` is bitwise left shift
- `>>` is bitwise right shift
- `~>>` is bitwise right shift (round)
- `^>>` is bitwise right shift (ceil)

With priority 15 (left-associative):
- `==` is integer equality check
- `!=` is integer inequality check
- `<` is integer comparison
- `<=` is integer comparison
- `>` is integer comparison
- `>=` is integer comparison
- `<=>` is integer comparison (returns -1, 0 or 1)

They also should be separated from the argument:
- `x + y` is ok
- `x+y` is not ok (it's a single identifier)

#### Conditional operator
It has the usual syntax.
```func
<condition> ? <consequence> : <alternative>
```
For example:
```func
x > 0 ? x * fac(x - 1) : 1;
```
It has priority 13.

#### Assignments
Priority 10.

Simple assignment `=` and counterparts of the binary operations: `+=`, `-=`, `*=`, `/=`, `~/=`, `^/=`, `%=`, `~%=`, `^%=`, `<<=`, `>>=`, `~>>=`, `^>>=`, `&=`, `|=`, `^=`.

## Loops
FunC supports `repeat`, `while`, and `do { ... } until` loops. The `for` loop is not supported.
### Repeat loop
The syntax is a `repeat` keyword followed by an expression of type `int`. Repeats the code for the specified number of times. Examples:
```func
int x = 1;
repeat(10) {
  x *= 2;
}
;; x = 1024
```
```func
int x = 1, y = 10;
repeat(y + 6) {
  x *= 2;
}
;; x = 65536
```
```func
int x = 1;
repeat(-1) {
  x *= 2;
}
;; x = 1
```
If the number of times is less than `-2^31` or greater than `2^31 - 1`, range check exception is thrown.
### While loop
Has the usual syntax. Example:
```func
int x = 2;
while (x < 100) {
  x = x * x;
}
;; x = 256
```
Note that the truth value of condition `x < 100` is of type `int` (cf. [absence of boolean type](/develop/func/types#absence-of-boolean-type)).

### Until loop
Has the following syntax:
```func
int x = 0;
do {
  x += 3;
} until (x % 17 == 0);
;; x = 51
```
## If statements
Examples:
```func
;; usual if
if (flag) {
  do_something();
}
```
```func
;; equivalent to if (~ flag)
ifnot (flag) {
  do_something();
}
```
```func
;; usual if-else
if (flag) {
  do_something();
}
else {
  do_alternative();
}
```
```func
;; Some specific features
if (flag1) {
  do_something1();
} else {
  do_alternative4();
}
```
The curly brackets are necessary. That code wouldn't be compiled:
```func
if (flag1)
  do_something();
```

## Try-Catch statements
*Available in func since v0.4.0*

Executes the code in `try` block. If it fails, completely rolls back changes made in `try` block and executes `catch` block instead; `catch` receives two arguments: the exception parameter of any type (`x`) and the error code (`n`, integer).

Unlike many other languages in the FunC try-catch statement, the changes made in the try block, in particular the modification of local and global variables, all registers' changes (i.e. `c4` storage register, `c5` action/message register, `c7` context register and others) **are discarded** if there is an error in the try block and consequently all contract storage updates and message sending will be reverted. It is important to note that some TVM state parameters such as _codepage_ and gas counters will not be rolled back. This means, in particular, that all gas spent in the try block will be taken into account, and the effects of OPs that change the gas limit (`accept_message` and `set_gas_limit`) will be preserved.

Note that exception parameter can be of any type (possibly different in case of different exceptions) and thus funC can not predict it on compile time. That means that developer need to "help" compiler by casting exception parameter to some type (see Example 2 below):

Examples:
```func
try {
  do_something();
} catch (x, n) {
  handle_exception();
}
```
```func
forall X -> int cast_to_int(X x) asm "NOP";
...
try {
  throw_arg(-1, 100);
} catch (x, n) {
  x.cast_to_int();
  ;; x = -1, n = 100
  return x + 1;
}
```
```func
int x = 0;
try {
  x += 1;
  throw(100);
} catch (_, _) {
}
;; x = 0 (not 1)
```

## Block statements
Block statements are also allowed. They open a new nested scope:
```func
int x = 1;
builder b = begin_cell();
{
  builder x = begin_cell().store_uint(0, 8);
  b = x;
}
x += 1;
```
