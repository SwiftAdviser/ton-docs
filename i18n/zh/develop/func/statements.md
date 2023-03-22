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
但是正如在全局變量[部分](/develop/func/global_variables.md)中提到的，全局變量不能重新聲明。

請注意，變量聲明是一個表達式語句，因此實際上像 `int x = 2` 這樣的構造是完整的表達式。例如，以下是正確的代碼：
```func
int y = (int x = 3) + 1;
```
它聲明了兩個變量 `x` 和 `y`，分別等於 `3` 和 `4`。
#### 底線
底線 `_` 用於不需要值的情況。例如，假設函數 `foo` 具有類型 `int -> (int, int, int)`。我們可以像這樣獲取第一個返回值，忽略第二個和第三個：
```func
(int fst, _, _) = foo(42);
```
### 函數應用
函數的調用在傳統語言中看起來像這樣。函數調用的參數在函數名稱之後列出，用逗號分隔。

```func
;; suppose foo has type (int, int, int) -> int
int x = foo(1, 2, 3);
```

但是請注意，`foo` 實際上是一個具有一個 `(int, int, int)` 類型的參數的函數。為了看到差異，假設 `bar` 是一個類型為 `int -> (int, int, int)` 的函數。與傳統語言不同，您可以像這樣組合函數：
```func
int x = foo(bar(42));
```
相反，其形式與類似但更冗長：
```func
(int a, int b, int c) = bar(42);
int x = foo(a, b, c);
```

也可以使用 Haskell 風格的調用方式，但不總是可行（稍後將進行修正）：
```func
;; suppose foo has type int -> int -> int -> int
;; i.e. it's carried
(int a, int b, int c) = (1, 2, 3);
int x = foo a b c; ;; ok
;; int y = foo 1 2 3; wouldn't compile
int y = foo (1) (2) (3); ;; ok
```
### 方法調用

#### 不可修改的方法
如果一個函數至少有一個參數，那麼它可以被調用為一個不可修改的方法。例如，`store_uint` 的類型為 `(builder, int, int) -> builder`（第二個參數是要存儲的值，第三個參數是位數）。`begin_cell` 是一個創建新 builder 的函數。以下代碼是等價的：
```func
builder b = begin_cell();
b = store_uint(b, 239, 8);
```
```func
builder b = begin_cell();
b = b.store_uint(239, 8);
```
所以函數的第一個參數可以在函數名之前使用 `.` 分隔，以傳遞給它。代碼可以進一步簡化：
```func
builder b = begin_cell().store_uint(239, 8);
```
也可以多次調用方法:
```func
builder b = begin_cell().store_uint(239, 8)
                        .store_int(-1, 16)
                        .store_uint(0xff, 10);
```
#### 修改方法
如果函數的第一個參數的類型為 `A`，且函數的返回值的形式為 `(A, B)`，其中 `B` 是某個任意類型，則此函數可以被調用為修改方法。修改方法調用可能需要一些參數並返回一些值，但它們修改了它們的第一個參數，也就是將返回值的第一個分量分配給第一個參數的變量。例如，假設 `cs` 是一個 cell slice，並且 `load_uint` 的類型為 `(slice, int) -> (slice, int)`：它接受一個 cell slice 和要加載的位數，並返回 slice 的其餘部分和加載的值。以下代碼是等價的：
```func
(cs, int x) = load_uint(cs, 8);
```
```func
(cs, int x) = cs.load_uint(8);
```
```func
int x = cs~load_uint(8);
```
在某些情況下，我們希望將函數用作修改方法，它不返回任何值，僅修改第一個參數。可以使用 unit 型來實現，方法如下：假設我們想要定義類型為 `int -> int` 的函數 `inc`，它將整數加 1，並將其用作修改方法。那麼我們應該將 `inc` 定義為類型 `int -> (int, ())` 的函數：
```func
(int, ()) inc(int x) {
  return (x + 1, ());
}
```
當定義為這樣時，它可以用作修改方法。下面的代碼將增加 `x` 的值。
```func
x~inc();
```

#### 函數名中的 `.` 和 `~`
假設我們也想要將 `inc` 作為一種非修改方法。我們可以這樣寫：
```func
(int y, _) = inc(x);
```
但是，可以覆蓋將 `inc` 定義為修改方法的定義。
```func
int inc(int x) {
  return x + 1;
}
(int, ()) ~inc(int x) {
  return (x + 1, ());
}
```
然後這樣調用它：
```func
x~inc();
int y = inc(x);
int z = x.inc();
```
第一個調用將修改 x ；第二個和第三個不會。

總之，當一個名為 `foo` 的函數作為一個非修改或修改方法調用時（即使用 `.foo` 或 `~foo` 語法），如果存在相應的 `.foo` 或 `~foo` 定義，則 FunC 編譯器將使用對應的定義，否則它使用 `foo` 的定義。

### 運算符
請注意，當前所有的一元和二元運算符都是整數運算符。邏輯運算符表示為按位整數運算符 (參見[布爾類型的缺失](/develop/func/types#absence-of-boolean-type))。
#### 一元運算符
有兩個一元運算符：
- `~` 是按位非運算符（優先級75）
- `-` 是整數求反運算符（優先級20）

它們應與參數分開：
- `- x` 正確。
- `-x` 不正確（它是單個標識符）

#### 二元運算符
具有優先級30（從左到右）：
- `*` 是整數乘法
- `/` 是整數除法（向下取整）
- `~/` 是整數除法（四捨五入）
- `^/` 是整數除法（向上取整）
- `%` 是整數模運算（向下取整）
- `~%` 是整數模運算（四捨五入）
- `^%` 是整數模運算（向上取整）
- `/%` 返回商和餘數
- `&` 是按位 AND

具有優先級20（從左到右）：
- `+` 是整數加法
- `-` 是整數減法
- `|` 是按位 OR
- `^` 是按位 XOR

具有優先級17（從左到右）：
- `<<` 是按位左移
- `>>` 是按位右移
- `~>>` 是按位右移（四捨五入）
- `^>>` 是按位右移（向上取整）

具有優先級15（從左到右）：
- `==` 是整數相等檢查
- `!=` 是整數不等檢查
- `<` 是整數比較
- `<=` 是整數比較
- `>` 是整數比較
- `>=` 是整數比較
- `<=>` 是整數比較（返回-1，0或1）

它們也應該與參數分開：
- `x + y` 正確
- `x+y` 不正確（它是一個單一的標識符）

#### 條件運算符
它具有通常的語法。
```func
<condition> ? <consequence> : <alternative>
```
例如：
```func
x > 0 ? x * fac(x - 1) : 1;
```
它的優先級是 13。

#### 賦值
優先級為 10。

簡單賦值 `=` 和二進制操作的對應物：`+=`、`-=`、`*=`、`/=`、`~/=`、`^/=`、`%=`、`~%=`、`^%=`、`<<=`、`>>=`、`~>>=`、`^>>=`、`&=`、`|=`、`^=`。

## Loops
FunC 支持 `repeat`、`while` 和 `do { ... } until` 循環。不支持 `for` 循環。

### Repeat 循環
語法是 `repeat` 關鍵字後跟一個 `int` 類型的表達式。重複執行指定次數的代碼。示例：
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
如果次數小於 `-2^31` 或大於 `2^31 - 1`，則會拋出範圍檢查異常。

### While 循環
具有通常的語法。例如：
```func
int x = 2;
while (x < 100) {
  x = x * x;
}
;; x = 256
```
需要注意的是，條件 `x < 100` 的真值類型是 `int`（參見[布爾類型的缺失](/develop/func/types#absence-of-boolean-type)）。

### Until 循環
具有以下語法：
```func
int x = 0;
do {
  x += 3;
} until (x % 17 == 0);
;; x = 51
```
## If 陳述句
範例：
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
需要使用花括號。下面的代碼無法編譯：
```func
if (flag1)
  do_something();
```

## Try-Catch 陳述句
*自 v0.4.0 起在 FunC 中可用*

執行 `try` 區塊中的代碼。如果失敗，將完全回滾 `try` 區塊中所做的更改，然後執行 `catch` 區塊。`catch` 接收兩個參數：任何類型的異常參數 (`x`) 和錯誤碼 (`n`，整數)。

不像許多其他語言，在 FunC 的 try-catch 語句中，對於在 try 區塊中進行的更改（特別是對於本地和全局變量的修改，所有註冊的更改（即 `c4` 存儲註冊，`c5` 操作/消息註冊，`c7` 上下文註冊等）**將被捨棄**，如果在 try 區塊中出現錯誤，所有合同存儲更新和消息發送都將被回滾。值得注意的是，某些 TVM 狀態參數（例如 _codepage_ 和 gas 計數器）將不會回滾。這意味著，特別是，在 try 區塊中花費的所有 gas 都將納入考慮，而更改 gas 限制的 OP 的影響（`accept_message` 和 `set_gas_limit`）將被保留。

需要注意的是，異常參數可以是任何類型（在不同的異常情況下可能不同），因此 funC 無法在編譯時預測異常參數的類型。這意味著開發人員需要通過將異常參數轉換為某些類型來“幫助”編譯器（請參見下面的示例 2）：

示例：
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

## 塊語句
也允許塊語句。它們打開一個新的嵌套作用域：
```func
int x = 1;
builder b = begin_cell();
{
  builder x = begin_cell().store_uint(0, 8);
  b = x;
}
x += 1;
```
