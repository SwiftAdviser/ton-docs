# FunC Cookbook

FunC Cookbook 的核心原因是將所有 FunC 開發人員的經驗集中在一個地方，以便未來的開發人員可以使用它！

相比 FunC 文檔，本文更注重解決智能合約開發過程中每個 FunC 開發人員的日常任務。

:::caution 草稿   
這是一篇概念性文章。我們仍在尋找有經驗的作者來撰寫它。閱讀有關在 [FunC Cookbook ton-footstep](https://github.com/ton-society/ton-footsteps/issues/10) 上做出貢獻的更多信息。
:::

## 基礎知識
### 如何編寫 if 語句

假設我們想檢查是否有任何事件是相關的。為此，我們使用標誌變量。請記住，在 FunC 中，`true` 是 `-1`，而 `false` 是 `0`。

```func
int flag = 0; ;; false

if (flag) { 
    ;; do something
}
else {
    ;; reject the transaction
}
```

> 💡 Noted
> 
> 我們不需要運算符 `==`，因為值 `0` 是 `false`，所以任何其他值都是 `true`。

> 💡 有用的鏈接
>  
> [文檔中的 "if 語句"](/develop/func/statements#if-statements)

### 如何編寫 repeat 循環

以指數運算為例

```func
int number = 2;
int multiplier = number;
int degree = 5;

repeat(degree - 1) {

    number *= multiplier;
}
```

> 💡 有用的鏈接
> 
> [文檔中的 "repeat 循環"](/develop/func/statements#repeat-loop)

### 如何編寫 while 循環

當我們不知道要執行特定操作的頻率時，while 循環非常有用。例如，取一個 `cell`，它知道最多可以存儲對其他單元格的四個引用。

```func
cell inner_cell = begin_cell() ;; create a new empty builder
        .store_uint(123, 16) ;; store uint with value 123 and length 16 bits
        .end_cell(); ;; convert builder to a cell

cell message = begin_cell()
        .store_ref(inner_cell) ;; store cell as reference
        .store_ref(inner_cell)
        .end_cell();

slice msg = message.begin_parse(); ;; convert cell to slice
while (msg.slice_refs_empty?() != -1) { ;; we should remind that -1 is true
    cell inner_cell = msg~load_ref(); ;; load cell from slice msg
    ;; do something
}
```

> 💡 有用的鏈接
> 
> [文檔中的 "while 循環"](/develop/func/statements#while-loop)
>
> [文檔中的 "cell"](/learn/overviews/cells)
>
> ["slice_refs_empty?()" 的文檔](/develop/func/stdlib#slice_refs_empty)
>
> ["store_ref()" 的文檔](/develop/func/stdlib#store_ref)
> 
> ["begin_cell()" 的文檔](/develop/func/stdlib#begin_cell)
> 
> ["end_cell()" 的文檔](/develop/func/stdlib#end_cell)
> 
> ["begin_parse()" 的文檔](/develop/func/stdlib#begin_parse)

### 如何編寫 do until 循環

當我們需要循環至少運行一次時，我們使用 `do until`。

```func 
int flag = 0;

do {
    ;; do something even flag is false (0) 
} until (flag == -1); ;; -1 is true
```

> 💡 有用的鏈接
> 
> [文檔中的 "until 循環"](/develop/func/statements#until-loop)

### 如何確定切片是否為空

在使用 `slice` 之前，必須檢查它是否有任何數據，以便正確處理它。我們可以使用 `slice_empty?()` 來做到這一點，但我們必須考慮到如果至少有一個 `bit` 數據或一個 `ref`，它會返回 `-1` (`true`)。

```func
;; creating empty slice
slice empty_slice = "";
;; `slice_empty?()` returns `true`, because slice dosen't have any `bits` and `refs`
empty_slice.slice_empty?();

;; creating slice which contains bits only
slice slice_with_bits_only = "Hello, world!";
;; `slice_empty?()` returns `false`, because slice have any `bits`
slice_with_bits_only.slice_empty?();

;; creating slice which contains refs only
slice slice_with_refs_only = begin_cell()
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_empty?()` returns `false`, because slice have any `refs`
slice_with_refs_only.slice_empty?();

;; creating slice which contains bits and refs
slice slice_with_bits_and_refs = begin_cell()
    .store_slice("Hello, world!")
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_empty?()` returns `false`, because slice have any `bits` and `refs`
slice_with_bits_and_refs.slice_empty?();
```
> 💡 有用的鏈接
>
> ["slice_empty?()" 的文檔](/develop/func/stdlib#slice_empty)
> 
> ["store_slice()" 的文檔](/develop/func/stdlib#store_slice)
> 
> ["store_ref()" 的文檔](/develop/func/stdlib#store_ref)
> 
> ["begin_cell()" 的文檔](/develop/func/stdlib#begin_cell)
> 
> ["end_cell()" 的文檔](/develop/func/stdlib#end_cell)
> 
> ["begin_parse()" 的文檔](/develop/func/stdlib#begin_parse)

### 如何判斷 slice 是否為空（不包含任何位，但可能包含引用）

如果我們只需要檢查 `bits`，並且不需要在 `slice` 中有任何 `refs`，則應使用 `slice_data_empty?()`。

```func 
;; creating empty slice
slice empty_slice = "";
;; `slice_data_empty?()` returns `true`, because slice dosen't have any `bits`
empty_slice.slice_data_empty?();

;; creating slice which contains bits only
slice slice_with_bits_only = "Hello, world!";
;; `slice_data_empty?()` returns `false`, because slice have any `bits`
slice_with_bits_only.slice_data_empty?();

;; creating slice which contains refs only
slice slice_with_refs_only = begin_cell()
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_data_empty?()` returns `true`, because slice dosen't have any `bits`
slice_with_refs_only.slice_data_empty?();

;; creating slice which contains bits and refs
slice slice_with_bits_and_refs = begin_cell()
    .store_slice("Hello, world!")
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_data_empty?()` returns `false`, because slice have any `bits`
slice_with_bits_and_refs.slice_data_empty?();
```

> 💡 有用的鏈接
>
> ["slice_data_empty?()" 的文檔](/develop/func/stdlib#slice_data_empty)
> 
> ["store_slice()" 的文檔](/develop/func/stdlib#store_slice)
> 
> ["store_ref()" 的文檔](/develop/func/stdlib#store_ref)
> 
> ["begin_cell()" 的文檔](/develop/func/stdlib#begin_cell)
> 
> ["end_cell()" 的文檔](/develop/func/stdlib#end_cell)
> 
> ["begin_parse()" 的文檔](/develop/func/stdlib#begin_parse)

### 如何確定片段是否為空（沒有任何引用，但可能具有位）

如果我們只對 `refs` 感興趣，則應使用 `slice_refs_empty?()` 檢查它們的存在。


```func 
;; creating empty slice
slice empty_slice = "";
;; `slice_refs_empty?()` returns `true`, because slice dosen't have any `refs`
empty_slice.slice_refs_empty?();

;; creating slice which contains bits only
slice slice_with_bits_only = "Hello, world!";
;; `slice_refs_empty?()` returns `true`, because slice dosen't have any `refs`
slice_with_bits_only.slice_refs_empty?();

;; creating slice which contains refs only
slice slice_with_refs_only = begin_cell()
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_refs_empty?()` returns `false`, because slice have any `refs`
slice_with_refs_only.slice_refs_empty?();

;; creating slice which contains bits and refs
slice slice_with_bits_and_refs = begin_cell()
    .store_slice("Hello, world!")
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_refs_empty?()` returns `false`, because slice have any `refs`
slice_with_bits_and_refs.slice_refs_empty?();
```

> 💡 有用的鏈接
> 
> ["slice_refs_empty?()" 在文檔中](/develop/func/stdlib#slice_refs_empty)
> 
> ["store_slice()" 在文檔中](/develop/func/stdlib#store_slice)
> 
> ["store_ref()" 在文檔中](/develop/func/stdlib#store_ref)
> 
> ["begin_cell()" 在文檔中](/develop/func/stdlib#begin_cell)
> 
> ["end_cell()" 在文檔中](/develop/func/stdlib#end_cell)
> 
> ["begin_parse()" 在文檔中](/develop/func/stdlib#begin_parse)

### 如何確定單元格是否為空

要檢查 `cell` 是否存在任何數據，我們應首先將其轉換為 `slice`。如果我們只對 `bits` 感興趣，則應使用 `slice_data_empty?()`；如果只對 `refs` 感興趣，則使用 `slice_data_refs?()`。如果我們希望檢查是否存在任何數據，而不管它是 `bit` 還是 `ref`，則需要使用 `slice_empty?()`。


```func
cell cell_with_bits_and_refs = begin_cell()
    .store_uint(1337, 16)
    .store_ref(null())
    .end_cell();

;; Change `cell` type to slice with `begin_parse()`
slice cs = cell_with_bits_and_refs.begin_parse();

;; determine if slice is empty
if (cs.slice_empty?()) {
    ;; cell is empty
}
else {
    ;; cell is not empty
}
```

> 💡 有用的鏈接
> 
> ["slice_empty?()" in docs](/develop/func/stdlib#slice_empty)
> 
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
> 
> ["store_uint()" in docs](/develop/func/stdlib#store_uint)
> 
> ["end_cell()" in docs](/develop/func/stdlib#end_cell)
> 
> ["begin_parse()" in docs](/develop/func/stdlib#begin_parse)

### 如何確定字典是否為空

有一種方法 `dict_empty?()` 可以檢查字典中的數據是否存在。這個方法相當於 `cell_null?()`，因為通常一個 `null` cell 就是一個空字典。


```func
cell d = new_dict();
d~udict_set(256, 0, "hello");
d~udict_set(256, 1, "world");

if (d.dict_empty?()) { ;; Determine if dict is empty
    ;; dict is empty
}
else {
    ;; dict is not empty
}
```

> 💡 有用的鏈接
>
> [文檔中的 "dict_empty?()"](/develop/func/stdlib#dict_empty)
>
> [文檔中的 "new_dict()"](/develop/func/stdlib/#new_dict) 創建一個空字典
>
> [文檔中的 "dict_set()"](/develop/func/stdlib/#dict_set) 使用函數在字典 d 中添加一些元素，使其不是空的

### 如何確定元組是否為空

在使用 `tuples` 時，始終知道是否存在任何值進行提取非常重要。如果我們嘗試從一個空的 `tuple` 中提取值，我們會收到一個錯誤：“not a tuple of valid size”，並且出現 `exit code 7`。


```func
;; Declare tlen function because it's not presented in stdlib
(int) tlen (tuple t) asm "TLEN";

() main () {
    tuple t = empty_tuple();
    t~tpush(13);
    t~tpush(37);

    if (t.tlen() == 0) {
        ;; tuple is empty
    }
    else {
        ;; tuple is not empty
    }
}
```

> 💡 Noted
> 
> 我們聲明了 tlen 組合語言函數。您可以在[這裡](/develop/func/functions#assembler-function-body-definition)閱讀更多信息，並查看[所有組合語言命令的列表](/learn/tvm-instructions/instructions)。

> 💡 有用的鏈接
>
> [文檔中的 "empty_tuple?()"](/develop/func/stdlib#empty_tuple)
>
> [文檔中的 "tpush()"](/develop/func/stdlib/#tpush)
>
> [文檔中的 "退出代碼"](/learn/tvm-instructions/tvm-exit-codes)

### 如何確定 lisp-style 列表是否為空

對於 Lisp-style 列表，可以使用 `empty_tuple?()` 函數來確定是否為空。如果是，那麼調用任何 `tpush()` 或 `tpop()` 函數都將導致 `exit code 7` 的異常。


```func
tuple numbers = null();
numbers = cons(100, numbers);

if (numbers.null?()) {
    ;; list-style list is empty
} else {
    ;; list-style list is not empty
}
```

We are adding number 100 to our list-style list with [cons](/develop/func/stdlib/#cons) function, so it's not empty.

### How to determine a state of the contract is empty

Let’s say we have a `counter` that stores the number of transactions. This variable is not available during the first transaction in the smart contract state, because the state is empty, so it is necessary to process such a case. If the state is empty, we create a variable `counter` and save it.

```func
;; `get_data()` will return the data cell from contract state
cell contract_data = get_data();
slice cs = contract_data.begin_parse();

if (cs.slice_empty?()) {
    ;; contract data is empty, so we create counter and save it
    int counter = 1;
    ;; create cell, add counter and save in contract state
    set_data(begin_cell().store_uint(counter, 32).end_cell());
}
else {
    ;; contract data is not empty, so we get our counter, increase it and save
    ;; we should specify correct length of our counter in bits
    int counter = cs~load_uint(32) + 1;
    set_data(begin_cell().store_uint(counter, 32).end_cell());
}
```

> 💡 Noted
> 
> We can determine that state of contract is empty by determining that [cell is empty](/develop/func/cookbook#how-to-determine-if-cell-is-empty).

> 💡 Useful links
>
> ["get_data()" in docs](/develop/func/stdlib#get_data)
>
> ["begin_parse()" in docs](/develop/func/stdlib/#begin_parse)
>
> ["slice_empty?()" in docs](/develop/func/stdlib/#slice_empty)
>
> ["set_data?()" in docs](/develop/func/stdlib#set_data)

### How to build an internal message cell

If we want the contract to send an internal message, we should first properly create it as a cell, specifying the technical flags, the recipient address, and the rest data.

```func
;; We use literal `a` to get valid address inside slice from string containing address 
slice addr = "EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx"a;
int amount = 1000000000;
;; we use `op` for identifying operations
int op = 0;

cell msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(amount)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
    .store_uint(op, 32)
.end_cell();

send_raw_message(msg, 3); ;; mode 3 - pay fees separately and ignore errors 
```

> 💡 Noted
>
> In this example, we use literal `a` to get address. You can find more about string literals in [docs](/develop/func/literals_identifiers#string-literals)

> 💡 Noted
>
> You can find more in [docs](/develop/smart-contracts/messages). Also, you can jump in [layout](/develop/smart-contracts/messages#message-layout) with this link.

> 💡 Useful links
>
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
> 
> ["store_uint()" in docs](/develop/func/stdlib#store_uint)
>
> ["store_slice()" in docs](/develop/func/stdlib#store_slice)
>
> ["store_coins()" in docs](/develop/func/stdlib#store_coins)
>
> ["end_cell()" in docs](/develop/func/stdlib/#end_cell)
>
> ["send_raw_message()" in docs](/develop/func/stdlib/#send_raw_message)

### How to contain a body as ref to an internal message cell

In the body of a message that follows flags and other technical data, we can send `int`, `slice`, and `cell`. In the case of the latter, it is necessary to set the bit to `1` before `store_ref()` to indicate that the `cell` will go on. 

We can also send the body of the message inside the same `cell` as header, if we are sure that we have enough space. In this case, we need to set the bit to `0`.

```func
;; We use literal `a` to get valid address inside slice from string containing address 
slice addr = "EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx"a;
int amount = 1000000000;
int op = 0;
cell message_body = begin_cell() ;; Creating a cell with message
    .store_uint(op, 32)
    .store_slice("❤")
.end_cell();
    
cell msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(amount)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1) 
    .store_uint(1, 1) ;; set bit to 1 to indicate that the cell will go on
    .store_ref(message_body)
.end_cell();

send_raw_message(msg, 3); ;; mode 3 - pay fees separately and ignore errors 
```

> 💡 Noted
>
> In this example, we use literal `a` to get address. You can find more about string literals in [docs](/develop/func/literals_identifiers#string-literals)

> 💡 Noted
>
> In this example, we used mode 3 to take the incoming tons and send exactly as much as specified (amount) while paying commission from the contract balance and ignoring the errors. Mode 64 is needed to return all the tons received, subtracting the commission, and mode 128 will send the entire balance.

> 💡 Noted
>
> We are [building a message](/develop/func/cookbook#how-to-build-an-internal-message-cell) but adding message body separetly.

> 💡 Useful links
>
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
> 
> ["store_uint()" in docs](/develop/func/stdlib#store_uint)
>
> ["store_slice()" in docs](/develop/func/stdlib#store_slice)
>
> ["store_coins()" in docs](/develop/func/stdlib#store_coins)
>
> ["end_cell()" in docs](/develop/func/stdlib/#end_cell)
>
> ["send_raw_message()" in docs](/develop/func/stdlib/#send_raw_message)

### How to contain a body as slice to an internal message cell

When sending messages, the body message can be sent either as `cell` or as `slice`. In this example, we send the body of the message inside the `slice`.

```func 
;; We use literal `a` to get valid address inside slice from string containing address 
slice addr = "EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx"a;
int amount = 1000000000;
int op = 0;
slice message_body = "❤"; 

cell msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(amount)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
    .store_uint(op, 32)
    .store_slice(message_body)
.end_cell();

send_raw_message(msg, 3); ;; mode 3 - pay fees separately and ignore errors 
```

> 💡 Noted
>
> In this example, we use literal `a` to get address. You can find more about string literals in [docs](/develop/func/literals_identifiers#string-literals)

> 💡 Noted
>
> In this example, we used mode 3 to take the incoming tons and send exactly as much as specified (amount) while paying commission from the contract balance and ignoring the errors. Mode 64 is needed to return all the tons received, subtracting the commission, and mode 128 will send the entire balance.

> 💡 Noted
>
> We are [building a message](/develop/func/cookbook#how-to-build-an-internal-message-cell) but adding message as a slice.

### How to iterate tuples (in both directions)

If we want to work with an array or stack in FunC, then tuple will be necessary there. And first of all we need to be able to iterate values to work with them.

```func
(int) tlen (tuple t) asm "TLEN";
forall X -> (tuple) to_tuple (X x) asm "NOP";

() main () {
    tuple t = to_tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    int len = t.tlen();
    
    int i = 0;
    while (i < len) {
        int x = t.at(i);
        ;; do something with x
        i = i + 1;
    }

    i = len - 1;
    while (i >= 0) {
        int x = t.at(i);
        ;; do something with x
        i = i - 1;
    }
}
```

> 💡 Noted
>
> We are declaring `tlen` assembly function. You can read more [here](/develop/func/functions#assembler-function-body-definition) and see [list of all assembler commands](/learn/tvm-instructions/instructions).
>
> Also we declaring `to_tuple` function. It just changes data type of any input to tuple, so be careful while using it.

### How to write own functions using `asm` keyword

When using any features we actually use pre-prepared for us methods inside `stdlib.fc`. But in fact, we have many more opportunities available to us, and we need to learn to write them ourselves.

For example, we have the method of `tpush`, which adds an element to `tuple`, but without `tpop`. In this case, we should do this:
```func
;; ~ means it is modifying method
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP"; 
```

If we want to know the length of `tuple` for iteration, we should write a new function with the `TLEN` asm instruction:
```func
int tuple_length (tuple t) asm "TLEN";
```

Some examples of functions already known to us from stdlib.fc:
```func
slice begin_parse(cell c) asm "CTOS";
builder begin_cell() asm "NEWC";
cell end_cell(builder b) asm "ENDC";
```

> 💡 Useful links:
>
> ["modifying method" in docs](/develop/func/statements#modifying-methods)
>
> ["stdlib" in docs](/develop/func/stdlib)
>
> ["TVM instructions" in docs](/learn/tvm-instructions/instructions)

### Iterating n-nested tuples

Sometimes we want to iterate nested tuples. The following example will iterate and print all of the items in a tuple of format `[[2,6],[1,[3,[3,5]]], 3]` starting from the head

```func
int tuple_length (tuple t) asm "TLEN";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";
forall X -> int is_tuple (X x) asm "ISTUPLE";
forall X -> tuple cast_to_tuple (X x) asm "NOP";
forall X -> int cast_to_int (X x) asm "NOP";
forall X -> (tuple) to_tuple (X x) asm "NOP";

;; define global variable
global int max_value;

() iterate_tuple (tuple t) impure {
    repeat (t.tuple_length()) {
        var value = t~tpop();
        if (is_tuple(value)) {
            tuple tuple_value = cast_to_tuple(value);
            iterate_tuple(tuple_value);
        }
        else {
            if(value > max_value) {
                max_value = value;
            }
        }
    }
}

() main () {
    tuple t = to_tuple([[2,6], [1, [3, [3, 5]]], 3]);
    int len = t.tuple_length();
    max_value = 0; ;; reset max_value;
    iterate_tuple(t); ;; iterate tuple and find max value
    ~dump(max_value); ;; 6
}
```

> 💡 Useful links
>
> ["Global variables" in docs](/develop/func/global_variables)
>
> ["~dump" in docs](/develop/func/builtins#dump-variable)
>
> ["TVM instructions" in docs](/learn/tvm-instructions/instructions) 


### Basic operations with tuples

```func
(int) tlen (tuple t) asm "TLEN";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";

() main () {
    ;; creating an empty tuple
    tuple names = empty_tuple(); 
    
    ;; push new items
    names~tpush("Naito Narihira");
    names~tpush("Shiraki Shinichi");
    names~tpush("Akamatsu Hachemon");
    names~tpush("Takaki Yuichi");
    
    ;; pop last item
    slice last_name = names~tpop();

    ;; get first item
    slice first_name = names.first();

    ;; get an item by index
    slice best_name = names.at(2);

    ;; getting the length of the list 
    int number_names = names.tlen();
}
```

### Resolving type X

The following example checks if some value is contained in a tuple, but tuple contains values X (cell, slice, int, tuple, int). We need to check the value and cast accordingly.

```func
forall X -> int is_null (X x) asm "ISNULL";
forall X -> int is_int (X x) asm "<{ TRY:<{ 0 PUSHINT ADD DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_cell (X x) asm "<{ TRY:<{ CTOS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_slice (X x) asm "<{ TRY:<{ SBITS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_tuple (X x) asm "ISTUPLE";
forall X -> int cast_to_int (X x) asm "NOP";
forall X -> cell cast_to_cell (X x) asm "NOP";
forall X -> slice cast_to_slice (X x) asm "NOP";
forall X -> tuple cast_to_tuple (X x) asm "NOP";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";

forall X -> () resolve_type (X value) impure {
    ;; value here is of type X, since we dont know what is the exact value - we would need to check what is the value and then cast it
    
    if (is_null(value)) {
        ;; do something with the null
    }
    elseif (is_int(value)) {
        int valueAsInt = cast_to_int(value);
        ;; do something with the int
    }
    elseif (is_slice(value)) {
        slice valueAsSlice = cast_to_slice(value);
        ;; do something with the slice
    }
    elseif (is_cell(value)) {
        cell valueAsCell = cast_to_cell(value);
        ;; do something with the cell
    }
    elseif (is_tuple(value)) {
        tuple valueAsTuple = cast_to_tuple(value);
        ;; do something with the tuple
    }
}

() main () {
    ;; creating an empty tuple
    tuple stack = empty_tuple();
    ;; let's say we have tuple and do not know the exact types of them
    stack~tpush("Some text");
    stack~tpush(4);
    ;; we use var because we do not know type of value
    var value = stack~tpop();
    resolve_type(value);
}
```

> 💡 Useful links
>
> ["TVM instructions" in docs](/learn/tvm-instructions/instructions) 


### How to get current time

```func
int current_time = now();
  
if (current_time > 1672080143) {
    ;; do some stuff 
}
```

### How to generate random number

:::caution draft
Please note that this method of generating random numbers isn't safe.

TODO: add link to an article about generating random numbers
:::

```func
randomize_lt(); ;; do this once

int a = rand(10);
int b = rand(1000000);
int c = random();
```

### Modulo operations

As an example, lets say that we want to run the following calculation of all 256 numbers : `(xp + zp)*(xp-zp)`. Since most of those operations are used for cryptography, in the following example we are using the modulo operator for montogomery curves.
Note that xp+zp is a valid variable name ( without spaces between ).

```func
(int) modulo_operations (int xp, int zp) {  
   ;; 2^255 - 19 is a prime number for montgomery curves, meaning all operations should be done against its prime
   int prime = 57896044618658097711785492504343953926634992332820282019728792003956564819949; 

   ;; muldivmod handles the next two lines itself
   ;; int xp+zp = (xp + zp) % prime;
   ;; int xp-zp = (xp - zp + prime) % prime;
   (_, int xp+zp*xp-zp) = muldivmod(xp + zp, xp - zp, prime);
   return xp+zp*xp-zp;
}
```

> 💡 Useful links
>
> ["muldivmod" in docs](/learn/tvm-instructions/instructions#52-division)


### How to throw errors

```func
int number = 198;

throw_if(35, number > 50); ;; the error will be triggered only if the number is greater than 50

throw_unless(39, number == 198); ;; the error will be triggered only if the number is NOT EQUAL to 198

throw(36); ;; the error will be triggered anyway
```

[Standard tvm exception codes](/learn/tvm-instructions/tvm-exit-codes.md)

### Reversing tuples

Because tuple stores data as a stack, sometimes we have to reverse tuple to read data from the other end.

```func
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";
int tuple_length (tuple t) asm "TLEN";
forall X -> (tuple) to_tuple (X x) asm "NOP";

(tuple) reverse_tuple (tuple t1) {
    tuple t2 = empty_tuple();
    repeat (t1.tuple_length()) {
        var value = t1~tpop();
        t2~tpush(value);
    }
    return t2;
}

() main () {
    tuple t = to_tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    tuple reversed_t = reverse_tuple(t);
    ~dump(reversed_t); ;; [10 9 8 7 6 5 4 3 2 1]
}
```

> 💡 Useful links
>
> ["tpush()" in docs](/develop/func/stdlib/#tpush)


### How to remove an item with a certain index from the list

```func
int tlen (tuple t) asm "TLEN";

(tuple, ()) remove_item (tuple old_tuple, int place) {
    tuple new_tuple = empty_tuple();

    int i = 0;
    while (i < old_tuple.tlen()) {
        int el = old_tuple.at(i);
        if (i != place) {
            new_tuple~tpush(el);
        }
        i += 1;  
    }
    return (new_tuple, ());
}

() main () {
    tuple numbers = empty_tuple();

    numbers~tpush(19);
    numbers~tpush(999);
    numbers~tpush(54);

    ~dump(numbers); ;; [19 999 54]

    numbers~remove_item(1); 

    ~dump(numbers); ;; [19 54]
}
```

### Determine if slices are equal

There are two different ways we can determine the equality. One is based on the slice hash, while the other one by using the SDEQ asm instruction.

```func
int are_slices_equal_1? (slice a, slice b) {
    return a.slice_hash() == b.slice_hash();
}

int are_slices_equal_2? (slice a, slice b) asm "SDEQ";

() main () {
    slice a = "Some text";
    slice b = "Some text";
    ~dump(are_slices_equal_1?(a, b)); ;; -1 = true

    a = "Text";
    ;; We use literal `a` to get valid address inside slice from string containing address
    b = "EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF"a;
    ~dump(are_slices_equal_2?(a, b)); ;; 0 = false
}
```

#### 💡 Useful links

 * ["slice_hash()" in docs](/develop/func/stdlib/#slice_hash)
 * ["SDEQ" in docs](/learn/tvm-instructions/instructions#62-other-comparison)

### Determine if cells are equal 

We can easily determine cell equality based on their hash.

```func
int are_cells_equal? (cell a, cell b) {
    return a.cell_hash() == b.cell_hash();
}

() main () {
    cell a = begin_cell()
            .store_uint(123, 16)
            .end_cell();

    cell b = begin_cell()
            .store_uint(123, 16)
            .end_cell();

    ~dump(are_cells_equal?(a, b)); ;; -1 = true
}
```

> 💡 Useful links
>
> ["cell_hash()" in docs](/develop/func/stdlib/#cell_hash)

### Determine if tuples are equal

A more advanced example would be to iterate and compare each of the tuple values. Since they are X we need to check and cast to the corresponding type and if it is tuple to iterate it recursively.

```func
int tuple_length (tuple t) asm "TLEN";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";
forall X -> int cast_to_int (X x) asm "NOP";
forall X -> cell cast_to_cell (X x) asm "NOP";
forall X -> slice cast_to_slice (X x) asm "NOP";
forall X -> tuple cast_to_tuple (X x) asm "NOP";
forall X -> int is_null (X x) asm "ISNULL";
forall X -> int is_int (X x) asm "<{ TRY:<{ 0 PUSHINT ADD DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_cell (X x) asm "<{ TRY:<{ CTOS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_slice (X x) asm "<{ TRY:<{ SBITS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_tuple (X x) asm "ISTUPLE";
int are_slices_equal? (slice a, slice b) asm "SDEQ";

int are_cells_equal? (cell a, cell b) {
    return a.cell_hash() == b.cell_hash();
}

(int) are_tuples_equal? (tuple t1, tuple t2) {
    int equal? = -1; ;; initial value to true
    
    if (t1.tuple_length() != t2.tuple_length()) {
        ;; if tuples are differ in length they cannot be equal
        return 0;
    }

    int i = t1.tuple_length();
    
    while (i > 0 & equal?) {
        var v1 = t1~tpop();
        var v2 = t2~tpop();
        
        if (is_null(t1) & is_null(t2)) {
            ;; nulls are always equal
        }
        elseif (is_int(v1) & is_int(v2)) {
            if (cast_to_int(v1) != cast_to_int(v2)) {
                equal? = 0;
            }
        }
        elseif (is_slice(v1) & is_slice(v2)) {
            if (~ are_slices_equal?(cast_to_slice(v1), cast_to_slice(v2))) {
                equal? = 0;
            }
        }
        elseif (is_cell(v1) & is_cell(v2)) {
            if (~ are_cells_equal?(cast_to_cell(v1), cast_to_cell(v2))) {
                equal? = 0;
            }
        }
        elseif (is_tuple(v1) & is_tuple(v2)) {
            ;; recursively determine nested tuples
            if (~ are_tuples_equal?(cast_to_tuple(v1), cast_to_tuple(v2))) {
                equal? = 0;
            }
        }
        else {
            equal? = 0;
        }

        i -= 1;
    }

    return equal?;
}

() main () {
    tuple t1 = cast_to_tuple([[2, 6], [1, [3, [3, 5]]], 3]);
    tuple t2 = cast_to_tuple([[2, 6], [1, [3, [3, 5]]], 3]);

    ~dump(are_tuples_equal?(t1, t2)); ;; -1 
}
```

> 💡 Useful links
>
> ["cell_hash()" in docs](/develop/func/stdlib/#cell_hash)
>
> ["TVM instructions" in docs](/learn/tvm-instructions/instructions)

### Generate internal address

We need to generate an internal address when our contract should deploy a new contract, but do not know his address. Suppose we already have `state_init` - the code and data of the new contract. 

Creates an internal address for the corresponding MsgAddressInt TLB.

```func
(slice) generate_internal_address (int workchain_id, cell state_init) {
    ;; addr_std$10 anycast:(Maybe Anycast) workchain_id:int8 address:bits256  = MsgAddressInt;

    return begin_cell()
        .store_uint(2, 2) ;; addr_std$10
        .store_uint(0, 1) ;; anycast nothing
        .store_int(workchain_id, 8) ;; workchain_id: -1
        .store_uint(cell_hash(state_init), 256)
    .end_cell().begin_parse();
}

() main () {
    slice deploy_address = generate_internal_address(workchain(), state_init);
    ;; then we can deploy new contract
}
```

> 💡 Noted
> 
> In this example, we use `workchain()` to get id of workchain. You can find more about Workchain ID in [docs](/learn/overviews/addresses#workchain-id).

> 💡 Useful links
>
> ["cell_hash()" in docs](/develop/func/stdlib/#cell_hash)

### Generate external address

Creates an external address for the corresponding MsgAddressExt TLB.

```func
slice generate_external_address (int address) {
    ;; addr_extern$01 len:(## 8) external_address:(bits len) = MsgAddressExt;
    
    int address_length = ubitsize(address);
    
    return begin_cell()
        .store_uint(1, 2) ;; addr_extern$01
        .store_uint(address_length, 8)
        .store_uint(address, address_length)
    .end_cell().begin_parse();
}

;; TODO: please provide an example how to use it
```

> 💡 Useful links
>
> TODO: please add useful links for all functions like in above sections 

### How to store and load dictionary in local storage

The logic for loading the dictionary

```func
slice local_storage = get_data().begin_parse();
cell dictionary_cell = new_dict();
if (~ slice_empty?(local_storage)) {
    dictionary_cell = local_storage~load_dict();
}
```

While the logic for storing the dictionary is like the following example:

```func
set_data(begin_cell().store_dict(dictionary_cell).end_cell());
```

> 💡 Useful links
>
> ["get_data()" in docs](/develop/func/stdlib/#get_data)
>
> ["new_dict()" in docs](/develop/func/stdlib/#new_dict)
>
> ["slice_empty?()" in docs](/develop/func/stdlib/#slice_empty)
>
> ["load_dict()" in docs](/develop/func/stdlib/#load_dict)
>
> ["~" in docs](/develop/func/statements#unary-operators)

### How to send a simple message

The usual way for us to send tons with a comment is actually a simple message. To specify that the body of the message is a `comment`, we should set `32 bits` before the message text to 0.

```func
cell msg = begin_cell()
    .store_uint(0x18, 6) ;; flags
    .store_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; destination address
    .store_coins(100) ;; amount of nanoTons to send
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; 107 zero-bits
    .store_uint(0, 32) ;; zero opcode - means simple transfer message with comment
    .store_slice("Hello from FunC!") ;; comment
.end_cell();
send_raw_message(msg, 3); ;; mode 3 - pay fees separately, ignore errors
```

> 💡 Useful links
>
> ["Message layout" in docs](/develop/smart-contracts/messages)

### How to send a message with an incoming account

The contract example below is useful to us if we need to perform any actions between the user and the main contract, that is, we need a proxy contract.

```func
() recv_internal (slice in_msg_body) {
    {-
        This is a simple example of a proxy-contract.
        It will expect in_msg_body to contain message mode, body and destination address to be sent to.
    -}

    int mode = in_msg_body~load_uint(8); ;; first byte will contain msg mode
    slice addr = in_msg_body~load_msg_addr(); ;; then we parse the destination address
    slice body = in_msg_body; ;; everything that is left in in_msg_body will be our new message's body

    cell msg = begin_cell()
        .store_uint(0x18, 6)
        .store_slice(addr)
        .store_coins(100) ;; just for example
        .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
        .store_slice(body)
    .end_cell();
    send_raw_message(msg, mode);
}
```

> 💡 Useful links
> 
> ["Message layout" in docs](/develop/smart-contracts/messages)
>
> ["load_msg_addr()" in docs](/develop/func/stdlib/#load_msg_addr)

### How to send a message with the entire balance

If we need to send the entire balance of the smart contract, then, in this case, we need to use send `mode 128`. An example of such a case would be a proxy contract that accepts payments and forwards to the main contract.

```func
cell msg = begin_cell()
    .store_uint(0x18, 6) ;; flags
    .store_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; destination address
    .store_coins(0) ;; we don't care about this value right now
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; 107 zero-bits
    .store_uint(0, 32) ;; zero opcode - means simple transfer message with comment
    .store_slice("Hello from FunC!") ;; comment
.end_cell();
send_raw_message(msg, 128); ;; mode = 128 is used for messages that are to carry all the remaining balance of the current smart contract
```

> 💡 Useful links
>
> ["Message layout" in docs](/develop/smart-contracts/messages)
> 
> ["Message modes" in docs](/develop/func/stdlib/#send_raw_message)

### How to send a message with a long text comment

As we know, only 127 characters can fit into a single `cell` (<1023 bits). In case we need more - we need to organize a snake cells.

```func
{-
    If we want to send a message with really long comment, we should split the comment to several slices.
    Each slice should have <1023 bits of data (127 chars).
    Each slice should have a reference to the next one, forming a snake-like structure.
-}

cell body = begin_cell()
    .store_uint(0, 32) ;; zero opcode - simple message with comment
    .store_slice("long long long message...")
    .store_ref(begin_cell()
        .store_slice(" you can store string of almost any length here.")
        .store_ref(begin_cell()
            .store_slice(" just don't forget about the 127 chars limit for each slice")
        .end_cell())
    .end_cell())
.end_cell();

cell msg = begin_cell()
    .store_uint(0x18, 6) ;; flags
    ;; We use literal `a` to get valid address inside slice from string containing address 
    .store_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; destination address
    .store_coins(100) ;; amount of nanoTons to send
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1) ;; 106 zero-bits, necessary for internal messages
    .store_uint(1, 1) ;; we want to store body as a ref
    .store_ref(body)
.end_cell();
send_raw_message(msg, 3); ;; mode 3 - pay fees separately, ignore errors
```

> 💡 Useful links
>
> ["Internal messages" in docs](/develop/smart-contracts/guidelines/internal-messages)

### How to get only data bits from a slice (without refs)

If we are not interested in `refs` inside the `slice`, then we can get a separate date and work with it.

```func
slice s = begin_cell()
    .store_slice("Some data bits...")
    .store_ref(begin_cell().end_cell()) ;; some references
    .store_ref(begin_cell().end_cell()) ;; some references
.end_cell().begin_parse();

slice s_only_data = s.preload_bits(s.slice_bits());
```

> 💡 Useful links
> 
> ["Slice primitives" in docs](/develop/func/stdlib/#slice-primitives)
>
> ["preload_bits()" in docs](/develop/func/stdlib/#preload_bits)
>
> ["slice_bits()" in docs](/develop/func/stdlib/#slice_bits)

### How to define your own modifying method

Modifying methods allow data to be modified within the same variable. This can be compared to referencing in other programming languages.

```func
(slice, (int)) load_digit (slice s) {
    int x = s~load_uint(8); ;; load 8 bits (one char) from slice
    x -= 48; ;; char '0' has code of 48, so we substract it to get the digit as a number
    return (s, (x)); ;; return our modified slice and loaded digit
}

() main () {
    slice s = "258";
    int c1 = s~load_digit();
    int c2 = s~load_digit();
    int c3 = s~load_digit();
    ;; here s is equal to "", and c1 = 2, c2 = 5, c3 = 8
}
```

> 💡 Useful links
> 
> ["Modifying methods" in docs](/develop/func/statements#modifying-methods)

### How to raise number to the power of n

```func
;; Unoptimized variant
int pow (int a, int n) {
    int i = 0;
    int value = a;
    while (i < n - 1) {
        a *= value;
        i += 1;
    }
    return a;
}

;; Optimized variant
(int) binpow (int n, int e) {
    if (e == 0) {
        return 1;
    }
    if (e == 1) {
        return n;
    }
    int p = binpow(n, e / 2);
    p *= p;
    if ((e % 2) == 1) {
        p *= n;
    }
    return p;
}

() main () {
    int num = binpow(2, 3);
    ~dump(num); ;; 8
}
```

### How to convert string to int

```func
slice string_number = "26052021";
int number = 0;

while (~ string_number.slice_empty?()) {
    int char = string_number~load_uint(8);
    number = (number * 10) + (char - 48); ;; we use ASCII table
}

~dump(number);
```

### How to convert int to string

```func
int n = 261119911;
builder string = begin_cell();
tuple chars = null();
do {
    int r = n~divmod(10);
    chars = cons(r + 48, chars);
} until (n == 0);
do {
    int char = chars~list_next();
    string~store_uint(char, 8);
} until (null?(chars));

slice result = string.end_cell().begin_parse();
~dump(result);
```

### How to iterate dictionaries

Dictionaries are very useful when working with a lot of data. We can get minimum and maximum key values using the built-in methods `dict_get_min?` and `dict_get_max?` respectively. Additionally, we can use `dict_get_next?` to iterate the dictionary.

```func
cell d = new_dict();
d~udict_set(256, 1, "value 1");
d~udict_set(256, 5, "value 2");
d~udict_set(256, 12, "value 3");

;; iterate keys from small to big
(int key, slice val, int flag) = d.udict_get_min?(256);
while (flag) {
    ;; do something with pair key->val
    
    (key, val, flag) = d.udict_get_next?(256, key);
}
```

> 💡 Useful links
>
> ["Dictonaries primitives" in docs](/develop/func/stdlib/#dictionaries-primitives)
>
> ["dict_get_max?()" in docs](/develop/func/stdlib/#dict_get_max)
>
> ["dict_get_min?()" in docs](/develop/func/stdlib/#dict_get_min)
>
> ["dict_get_next?()" in docs](/develop/func/stdlib/#dict_get_next)
>
> ["dict_set()" in docs](/develop/func/stdlib/#dict_set)

### How to delete value from dictionaries

```func
cell names = new_dict();
names~udict_set(256, 27, "Alice");
names~udict_set(256, 25, "Bob");

names~udict_delete?(256, 27);

(slice val, int key) = names.udict_get?(256, 27);
~dump(val); ;; null() -> means that key was not found in a dictionary
```

### How to iterate cell tree recursively

As we know, one `cell` can store up to `1023 bits` of data and up to `4 refs`. To get around this limit, we can use a tree of cells, but to do this we need to be able to iterate it for proper data processing.

```func
forall X -> int is_null (X x) asm "ISNULL";
forall X -> (tuple, ()) push_back (tuple tail, X head) asm "CONS";
forall X -> (tuple, (X)) pop_back (tuple t) asm "UNCONS";

() main () {
    ;; just some cell for example
    cell c = begin_cell()
        .store_uint(1, 16)
        .store_ref(begin_cell()
            .store_uint(2, 16)
        .end_cell())
        .store_ref(begin_cell()
            .store_uint(3, 16)
            .store_ref(begin_cell()
                .store_uint(4, 16)
            .end_cell())
            .store_ref(begin_cell()
                .store_uint(5, 16)
            .end_cell())
        .end_cell())
    .end_cell();

    ;; creating tuple with no data, which plays the role of stack
    tuple stack = null();
    ;; bring the main cell into the stack to process it in the loop
    stack~push_back(c);
    ;; do it until stack is not null
    while (~ stack.is_null()) {
        ;; get the cell from the stack and convert it to a slice to be able to process it
        slice s = stack~pop_back().begin_parse();

        ;; do something with s data

        ;; if the current slice has any refs, add them to stack
        repeat (s.slice_refs()) {
            stack~push_back(s~load_ref());
        }
    }
}
```

> 💡 Useful links
> 
> ["Lisp-style lists" in docs](/develop/func/stdlib/#lisp-style-lists)
>
> ["null()" in docs](/develop/func/stdlib/#null)
>
> ["slice_refs()" in docs](/develop/func/stdlib/#slice_refs)

### How to iterate through lisp-style list

The data type tuple can hold up to 255 values. If this is not enough, then we should use a lisp-style list. We can put a tuple inside a tuple, thus bypassing the limit.

```func
forall X -> int is_null (X x) asm "ISNULL";
forall X -> (tuple, ()) push_back (tuple tail, X head) asm "CONS";
forall X -> (tuple, (X)) pop_back (tuple t) asm "UNCONS";

() main () {
    ;; some example list
    tuple l = null();
    l~push_back(1);
    l~push_back(2);
    l~push_back(3);

    ;; iterating through elements
    ;; note that this iteration is in reversed order
    while (~ l.is_null()) {
        var x = l~pop_back();

        ;; do something with x
    }
}
```

> 💡 Useful links
> 
> ["Lisp-style lists" in docs](/develop/func/stdlib/#lisp-style-lists)
>
> ["null()" in docs](/develop/func/stdlib/#null)

### How to send a deploy message (with stateInit only, with stateInit and body)

```func
() deploy_with_stateinit(cell message_header, cell state_init) impure {
  var msg = begin_cell()
    .store_slice(begin_parse(msg_header))
    .store_uint(2 + 1, 2) ;; init:(Maybe (Either StateInit ^StateInit))
    .store_uint(0, 1) ;; body:(Either X ^X)
    .store_ref(state_init)
    .end_cell();

  ;; mode 64 - carry the remaining value in the new message
  send_raw_message(msg, 64); 
}

() deploy_with_stateinit_body(cell message_header, cell state_init, cell body) impure {
  var msg = begin_cell()
    .store_slice(begin_parse(msg_header))
    .store_uint(2 + 1, 2) ;; init:(Maybe (Either StateInit ^StateInit))
    .store_uint(1, 1) ;; body:(Either X ^X)
    .store_ref(state_init)
    .store_ref(body)
    .end_cell();

  ;; mode 64 - carry the remaining value in the new message
  send_raw_message(msg, 64); 
}
```

### How to build a stateInit cell

```func
() build_stateinit(cell init_code, cell init_data) {
  var state_init = begin_cell()
    .store_uint(0, 1) ;; split_depth:(Maybe (## 5))
    .store_uint(0, 1) ;; special:(Maybe TickTock)
    .store_uint(1, 1) ;; (Maybe ^Cell)
    .store_uint(1, 1) ;; (Maybe ^Cell)
    .store_uint(0, 1) ;; (HashmapE 256 SimpleLib)
    .store_ref(init_code)
    .store_ref(init_data)
    .end_cell();
}
```

### How to calculate a contract address (using stateInit)

```func
() calc_address(cell state_init) {
  var future_address = begin_cell() 
    .store_uint(2, 2) ;; addr_std$10
    .store_uint(0, 1) ;; anycast:(Maybe Anycast)
    .store_uint(0, 8) ;; workchain_id:int8
    .store_uint(cell_hash(state_init), 256) ;; address:bits256
    .end_cell();
}
```
