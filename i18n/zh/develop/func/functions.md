# 函數

FunC程式本質上是一個函數聲明/定義和全域變數聲明的列表。本節將涵蓋第一個主題。

任何函數聲明或定義都以一個共同的模式開始，接著有三種情況之一：

* 單獨的`;`，這意味著函數被聲明但尚未定義。它可以在同一文件中或在當前文件之前傳遞的其他文件中定義。例如，
  ```func
  int add(int x, int y);
  ```
  是一個名為 `add` 、型別為 `(int, int) -> int` 的函數簡單聲明。
- 組合語言函數體定義。這是使用低級TVM原語定義函數以供稍後在FunC程序中使用的方法。例如，
  ```func
  int add(int x, int y) asm "ADD";
  ```
  是同一函數 `add` 的組合語言定義，型別為 `(int, int) -> int` ，它將被編譯為TVM操作碼 `ADD` 。

- 普通區塊語句函數體定義。這是定義函數的常規方式。例如，
  ```func
  int add(int x, int y) {
    return x + y;
  }
  ```
  是函數 `add` 的普通定義方式。

## 函式宣告
如前所述，任何函式的宣告或定義都以共同的模式開始。以下是此模式：
```func
[<forall declarator>] <return_type> <function_name>(<comma_separated_function_args>) <specifiers>
```
其中 `[ ... ]` 代表一個可選的項目。


### 函式名稱

函式名稱可以是任何[識別字元](https://chat.openai.com/develop/func/literals_identifiers#identifiers)，並且可以以 `.` 或 `~` 符號開頭。這些符號的意義在[陳述式](https://chat.openai.com/develop/func/statements#methods-calls)中有所解釋。

例如，`udict_add_builder?`、`dict_set`和`~dict_set`都是有效且不同的函式名稱（它們定義在[stdlib.fc](https://chat.openai.com/develop/func/stdlib)中）。

#### 特殊函式名稱

FunC（實際上是Fift組合語言）有幾個保留的函式名稱，具有預定義的[id](https://chat.openai.com/develop/func/functions#method_id)。

* `main`和`recv_internal`具有id = 0
* `recv_external`具有id = -1
* `run_ticktock`具有id = -2

每個程序都必須具有帶有id 0的函式，即`main`或`recv_internal`函式。 在特殊智能合約的ticktock交易中，會調用`run_ticktock`。

#### 接收內部消息

當智能合約收到入站的內部消息時，會調用`recv_internal`函式。在[TVM初始化](https://ton.org/docs/learn/tvm-instructions/tvm-overview#initialization-of-tvm)時，堆疊中會有一些變數。通過在`recv_internal`中設置參數，我們可以讓智能合約代碼了解其中的一些變數。對於代碼不知道的參數，它們只會位於堆疊的底部，從未被使用。

因此，以下每個`recv_internal`的聲明都是正確的，但那些使用更少變數的聲明會稍微節省一些 gas（每個未使用的參數都會增加額外的`DROP`指令）。

```func
() recv_internal(int balance, int msg_value, cell in_msg_cell, slice in_msg) {}
() recv_internal(int msg_value, cell in_msg_cell, slice in_msg) {}
() recv_internal(cell in_msg_cell, slice in_msg) {}
() recv_internal(slice in_msg) {}
```




#### 接收外部消息

`recv_external`是用於接收入站的外部消息。

### 回傳型別

回傳型別可以是[型別](https://chat.openai.com/develop/func/types.md)章節中所述的任何原子或複合型別。例如，
```func
int foo();
(int, int) foo'();
[int, int] foo''();
(int -> int) foo'''();
() foo''''();
```
都是有效的函式宣告。

Type inference is also allowed. For example,
```func
_ pyth(int m, int n) {
  return (m * m - n * n, 2 * m * n, m * m + n * n);
}
```
是一個有效的函式定義，函式名稱為 `pyth` ，型別為 `(int, int) -> (int, int, int)` ，用於計算勾股數。

### 函式參數

函式參數由逗號分隔。以下是參數的有效聲明方式：

* 普通聲明：類型 + 名稱。例如，在函式聲明 `() foo(int x);` 中，`int x` 是類型為 `int`、名稱為 `x` 的參數聲明。
* 未使用的參數聲明：僅類型。例如，
  ```func
  int first(int x, int) {
    return x;
  }
  ```
  是一個有效的函式定義，型別為 `(int, int) -> int`。
* 具有推斷型別聲明的參數：僅名稱。 例如，
  ```func
  int inc(x) {
    return x + 1;
  }
  ```
  是一個有效的函式定義，型別為 int -> int。 x 的 int 型別由類型檢查器推斷。

需要注意的是，儘管一個函式看起來像是多個參數的函式，但實際上它是一個以單一 [張量型別](https://chat.openai.com/develop/func/types#tensor-types) 參數的函式。要了解這種差異，請參閱[函式應用](https://chat.openai.com/develop/func/statements#function-application)。儘管如此，參數張量的組成部分通常被稱為函式參數。

### 函式呼叫

#### 非修改方法

:::info

非修改函式支援使用 `.` 進行簡潔的函式呼叫。

:::

```func
example(a);
a.example();
```

如果一個函式至少有一個參數，它可以被當作一個非修改方法進行調用。例如，`store_uint` 的型別為 `(builder, int, int) -> builder` （第二個參數是要存儲的值，第三個是位長度）。`begin_cell` 是一個創建新 builder 的函式。以下代碼等效：

```func
builder b = begin_cell();
b = store_uint(b, 239, 8);
```

```func
builder b = begin_cell();
b = b.store_uint(239, 8);
```
因此，函式的第一個參數可以在函式名稱之前通過 . 分隔傳遞給它。該代碼可以進一步簡化：

```func
builder b = begin_cell().store_uint(239, 8);
```
Multiple calls of methods are also possible:
```func
builder b = begin_cell().store_uint(239, 8)
                        .store_int(-1, 16)
                        .store_uint(0xff, 10);
```


#### 修改函式

:::info 修改函式支援使用 `~` 和 `.` 運算子進行簡化呼叫。 :::

如果一個函式的第一個參數型別為 `A`，而函式的返回值形狀為 `(A, B)`，其中 `B` 是任意型別，那麼此函式可以被當作一個修改方法來調用。

修改函式的呼叫可能會有一些參數和返回值，但它們會修改它們的第一個參數，即將返回值的第一個元素賦值給第一個參數的變數。

```func
a~example();
a = example(a);
```


例如，假設 `cs` 是一個 cell slice，而 `load_uint` 的型別為 `(slice, int) -> (slice, int)` ：它接受一個 cell slice 和要加載的位數，並返回切片的剩餘部分和已加載的值。以下代碼等效：
```func
(cs, int x) = load_uint(cs, 8);
```
```func
(cs, int x) = cs.load_uint(8);
```
```func
int x = cs~load_uint(8);
```
在某些情況下，我們想使用一個不返回任何值，只修改第一個參數的函式作為修改方法。可以使用單位型別來實現，如下所示：假設我們想定義型別為 int -> int 的函式 inc，它將整數加1，並將其作為修改方法使用。那麼我們應該將 inc 定義為型別為 int -> (int, ()) 的函式：

```func
(int, ()) inc(int x) {
  return (x + 1, ());
}
```
這樣定義後，可以將它用作修改方法。以下代碼將會將 `x` 加1。

```func
x~inc();
```

#### 函式名稱中的 `.` 和 `~`

假設我們希望將 `inc` 用作一個非修改方法。我們可以寫出類似這樣的程式碼：
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



### Specifiers
There are three types of specifiers: `impure`, `inline`/`inline_ref`, and `method_id`. One, several, or none of them can be put in a function declaration but currently they must be presented in the right order. For example, it is not allowed to put `impure` after `inline`.
#### Impure specifier
`impure` specifier means that the function can have some side effects which can't be ignored. For example, we should put `impure` specifier if the function can modify contract storage, send messages, or throw an exception when some data is invalid and the function is intended to validate this data.

If `impure` is not specified and the result of the function call is not used, then the FunC compiler may and will delete this function call.

For example, in the [stdlib.fc](/develop/func/stdlib) function
```func
int random() impure asm "RANDU256";
```
is defined. `impure` is used because `RANDU256` changes the internal state of the random number generator.

#### Inline specifier
If a function has `inline` specifier, its code is actually substituted in every place where the function is called. It goes without saying that recursive calls to inlined functions are not possible.

For example, you can using `inline` like this way in this example: [ICO-Minter.fc](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/ft/jetton-minter-ICO.fc#L16)

```func
() save_data(int total_supply, slice admin_address, cell content, cell jetton_wallet_code) impure inline {
  set_data(begin_cell()
            .store_coins(total_supply)
            .store_slice(admin_address)
            .store_ref(content)
            .store_ref(jetton_wallet_code)
           .end_cell()
          );
}
```


#### Inline_ref specifier
The code of a function with the `inline_ref` specifier is put into a separate cell, and every time when the function is called, a `CALLREF` command is executed by TVM. So it's similar to `inline`, but because a cell can be reused in several places without duplicating it, it is almost always more efficient in terms of code size to use `inline_ref` specifier instead of `inline` unless the function is called exactly once. Recursive calls of `inline_ref`'ed functions are still impossible because there are no cyclic references in the TVM cells.
#### method_id
Every function in TVM program has an internal integer id by which it can be called. Ordinary functions are usually numbered by subsequent integers starting from 1, but get-methods of the contract are numbered by crc16 hashes of their names. `method_id(<some_number>)` specifier allows to set the id of a function to specified value, and `method_id` uses the default value `(crc16(<function_name>) & 0xffff) | 0x10000`. If a function has `method_id` specifier, then it can be called in lite-client or ton-explorer as a get-method by its name.

For example,
```func
(int, int) get_n_k() method_id {
  (_, int n, int k, _, _, _, _) = unpack_state();
  return (n, k);
}
```
is a get-method of multisig contract.

### Polymorphism with forall
Before any function declaration or definition, there can be `forall` type variables declarator. It has the following syntax:
```func
forall <comma_separated_type_variables_names> ->
```
where type variable name can be any [identifier](/develop/func/literals_identifiers#identifiers). Usually, they are named with capital letters.

For example,
```func
forall X, Y -> [Y, X] pair_swap([X, Y] pair) {
  [X p1, Y p2] = pair;
  return [p2, p1];
}
```
is a function that takes a tuple of length exactly 2, but with values of any (single stack entry) types in components, and swaps them with each other.

`pair_swap([2, 3])` will produce `[3, 2]` and `pair_swap([1, [2, 3, 4]])` will produce `[[2, 3, 4], 1]`.

In this example `X` and `Y` are [type variables](/develop/func/types#polymorphism-with-type-variables). When the function is called, type variables are substituted with actual types, and the code of the function is executed. Note that although the function is polymorphic, the actual assembler code for it is the same for every type substitution. It is achieved essentially by the polymorphism of stack manipulation primitives. Currently, other forms of polymorphism (like ad-hoc polymorphism with type classes) are not supported.

Also, it is worth noticing that the type width of `X` and `Y` is supposed to be equal to 1; that is, the values of `X` or `Y` must occupy a single stack entry. So you actually can't call the function `pair_swap` on a tuple of type `[(int, int), int]`, because type `(int, int)` has width 2, i.e., it occupies 2 stack entries.



## Assembler function body definition
As mentioned above, a function can be defined by the assembler code. The syntax is an `asm` keyword followed by one or several assembler commands, represented as strings.
For example, one can define:
```func
int inc_then_negate(int x) asm "INC" "NEGATE";
```
– a function that increments an integer and then negates it. Calls to this function will be translated to 2 assembler commands `INC` and `NEGATE`. Alternative way to define the function is:
```func
int inc_then_negate'(int x) asm "INC NEGATE";
```
`INC NEGATE` will be considered by FunC as one assembler command, but it is OK, because Fift assembler knows that it is 2 separate commands.

:::info
The list of assembler commands can be found here: [TVM instructions](/learn/tvm-instructions/instructions).
:::

### Rearranging stack entries
In some cases, we want to pass arguments to the assembler function in a different order than the assembler command requires, or/and take the result in a different stack entry order than the command returns. We could manually rearrange the stack by adding corresponding stack primitives, but FunC can do it automatically.

:::info
Note, that in case of manual rearranging, arguments will be computed in the rearranged order. To overwrite this behavior use `#pragma compute-asm-ltr`: [compute-asm-ltr](compiler_directives#pragma-compute-asm-ltr)
:::

For example, suppose that the assembler command STUXQ takes an integer, builder, and integer; then it returns the builder, along with the integer flag, indicating the success or failure of the operation.
We may define the function:
```func
(builder, int) store_uint_quite(int x, builder b, int len) asm "STUXQ";
```
However, suppose we want to rearrange arguments. Then we can define:
```func
(builder, int) store_uint_quite(builder b, int x, int len) asm(x b len) "STUXQ";
```
So you can indicate the required order of arguments after the `asm` keyword.

Also, we can rearrange return values like this:
```func
(int, builder) store_uint_quite(int x, builder b, int len) asm( -> 1 0) "STUXQ";
```
The numbers correspond to the indexes of returned values (0 is the deepest stack entry among returned values).

Combining this techniques is also possible.
```func
(int, builder) store_uint_quite(builder b, int x, int len) asm(x b len -> 1 0) "STUXQ";
```

### Multiline asms
Multiline assembler command or even Fift-code snippets can be defined via multiline strings which starts and ends with `"""`.

```func
slice hello_world() asm """
  "Hello"
  " "
  "World"
  $+ $+ $>s
  PUSHSLICE
""";
```
