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
但是，我們可以覆寫 `inc` 作為修改方法的定義。
```func
int inc(int x) {
  return x + 1;
}
(int, ()) ~inc(int x) {
  return (x + 1, ());
}
```
然後可以像這樣呼叫它：
```func
x~inc();
int y = inc(x);
int z = x.inc();
```
第一個呼叫將修改 x，而第二個和第三個則不會。

總之，當以非修改或修改方法的方式調用名為 `foo` 的函式（即使用 `.foo` 或 `~foo` 語法）時，FunC 編譯器會相應地使用 `.foo` 或 `~foo` 的定義，如果有這樣的定義存在，否則它會使用 `foo` 的定義。


### 修飾符

有三種類型的修飾符：`impure`、`inline`/`inline_ref` 和 `method_id`。一個函式宣告中可以有一個、多個或沒有這些修飾符，但目前它們必須按正確的順序呈現。例如，不允許在 `inline` 之後放置 `impure`。

#### Impure 修飾符

`impure` 修飾符表示該函式可能具有一些不可忽略的副作用。例如，如果函式可以修改合約存儲、發送消息或在某些數據無效時引發異常，並且該函式旨在驗證這些數據，則應該放置 `impure` 修飾符。

如果沒有指定 `impure`，並且函式調用的結果未被使用，那麼 FunC 編譯器可能會刪除此函式調用。

例如，在 [stdlib.fc](https://chat.openai.com/develop/func/stdlib) 函式中：
```func
int random() impure asm "RANDU256";
```
定義了 `impure`，因為 `RANDU256` 改變了隨機數生成器的內部狀態。

#### Inline 修飾符

如果函式有 `inline` 修飾符，則它的代碼實際上會在調用函式的每個地方替換。不用說，內聯函式的遞歸調用是不可能的。

例如，在此範例中可以這樣使用 `inline`：[ICO-Minter.fc](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/ft/jetton-minter-ICO.fc#L16)

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


#### Inline_ref 修飾符

具有 `inline_ref` 修飾符的函式的代碼被放入一個單獨的儲存格中，每當該函式被調用時，TVM 就會執行 `CALLREF` 命令。因此，它類似於 `inline`，但由於可以在多個位置重複使用儲存格，而不會重複，所以在代碼大小方面使用 `inline_ref` 修飾符通常比使用 `inline` 更有效，除非函式確實只被調用了一次。在 TVM 儲存格中，不存在循環引用，因此仍然無法進行 `inline_ref` 函式的遞迴調用。

#### method_id

TVM 程序中的每個函式都有一個內部整數 ID，可以通過該 ID 進行調用。通常，普通函式的 ID 是從 1 開始的連續整數，但合約的 get 方法是根據它們的名稱的 crc16 哈希編號的。`method_id(<some_number>)` 修飾符允許將函式的 ID 設置為指定的值，而 `method_id` 則使用默認值 `(crc16(<function_name>) & 0xffff) | 0x10000`。如果一個函式具有 `method_id` 修飾符，那麼可以通過其名稱在 lite-client 或 ton-explorer 中將其作為 get 方法調用。

例如：

```func
(int, int) get_n_k() method_id {
  (_, int n, int k, _, _, _, _) = unpack_state();
  return (n, k);
}
```
是多重簽名合約的一個 get 方法。

### 使用 forall 實現多型

在任何函式宣告或定義之前，都可以有 `forall` 類型變數聲明。它具有以下語法：
```func
forall <comma_separated_type_variables_names> ->
```
其中，型別變數名稱可以是任何 [識別符](/develop/func/literals_identifiers#identifiers)。通常，它們以大寫字母命名。

For example,
```func
forall X, Y -> [Y, X] pair_swap([X, Y] pair) {
  [X p1, Y p2] = pair;
  return [p2, p1];
}
```
此函數接收一個元素長度為 2 的元組，且其組成部分可以是任何 (單一堆棧) 類型的值，將其互換後返回。

`pair_swap([2, 3])` 將會產生 `[3, 2]`，而 `pair_swap([1, [2, 3, 4]])` 將會產生 `[[2, 3, 4], 1]`。

在這個例子中，`X` 和 `Y` 是 [型別變數](/develop/func/types#polymorphism-with-type-variables)。當函數被呼叫時，型別變數會被實際的型別取代，並執行函數的程式碼。需要注意的是，儘管此函數是多型的，但它的組合語言程式碼對於每個型別取代來說都是相同的。這主要是通過堆疊操作基元的多型實現的。目前，不支援其他形式的多型（例如具有型別類別的特定多型）。


此外，值得注意的是，`X` 和 `Y` 的型別寬度應該等於 1；也就是說，`X` 或 `Y` 的值必須佔用單個堆疊項目。因此，實際上無法將型別為 `[(int, int), int]` 的元組傳遞給函數 `pair_swap`，因為型別 `(int, int)` 的寬度為 2，即它佔用 2 個堆疊項目。



## 組合語言函數體定義
如上所述，可以使用組合語言程式碼來定義函數。語法是 `asm` 關鍵字後跟一個或多個組合語言指令，以字符串表示。
例如，可以定義：
```func
int inc_then_negate(int x) asm "INC" "NEGATE";
```
– 一個將整數加一並取相反數的函數。對該函數的調用將被轉換為 2 條組合語言指令 `INC` 和 `NEGATE`。另一種定義該函數的方式是：
```func
int inc_then_negate'(int x) asm "INC NEGATE";
```
`INC NEGATE` will be considered by FunC as one assembler command, but it is OK, because Fift assembler knows that it is 2 separate commands.

:::info
組合語言指令的列表可以在此處找到：[TVM 指令](/learn/tvm-instructions/instructions)。
:::

### 重新排列堆疊項目
在某些情況下，我們希望以不同於組合語言指令要求的順序傳遞參數給組合語言函數，或者/和以不同的堆疊項目順序取得結果。我們可以通過添加相應的堆疊基元來手動重新排列堆疊，但是 FunC 可以自動執行這個過程。

:::info
需要注意的是，在手動重新排列的情況下，參數將按照重新排列的順序進行計算。若要覆蓋此行為，使用 `#pragma compute-asm-ltr`：[compute-asm-ltr](compiler_directives#pragma-compute-asm-ltr)
:::

例如，假設組合語言指令 STUXQ 接受一個整數、構建器和整數；然後它將返回構建器以及表示操作成功或失敗的整數標誌。
我們可以定義函數：
```func
(builder, int) store_uint_quite(int x, builder b, int len) asm "STUXQ";
```
但是，假設我們想要重新排列參數。那麼，我們可以這樣定義：
```func
(builder, int) store_uint_quite(builder b, int x, int len) asm(x b len) "STUXQ";
```
因此，您可以在 `asm` 關鍵字後面指定所需的參數順序。

此外，我們可以這樣重新排列返回值：
```func
(int, builder) store_uint_quite(int x, builder b, int len) asm( -> 1 0) "STUXQ";
```
這些數字對應於返回值的索引（0 是返回值中最深的堆疊項目）。

結合這些技術也是可能的。
```func
(int, builder) store_uint_quite(builder b, int x, int len) asm(x b len -> 1 0) "STUXQ";
```

### 多行組合語言指令

可以使用以 `"""` 開始和結束的多行字串來定義多行組合語言指令，甚至可以定義 Fift 代碼片段。

```func
slice hello_world() asm """
  "Hello"
  " "
  "World"
  $+ $+ $>s
  PUSHSLICE
""";
```
