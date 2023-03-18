# 文字面量和標識符
## 數字字面量
FunC 允許使用十進制和十六進制整數字面量（允許前導零）。

例如，`0`，`123`，`-17`，`00987`，`0xef`，`0xEF`，`0x0`，`-0xfFAb`，`0x0001`，`-0`，`-0x0` 都是有效的數字字面量。

## 字符串字面量
在 FunC 中，字符串使用雙引號 `"` 括起來，例如 `"這是一個字符串"`。不支持特殊符號，如 `\n` 和多行字符串。
可選擇地，字符串字面量可以在其後指定一個類型，例如 `"字符串"u`。


以下字符串類型得到了支持：
* 沒有類型—用於 asm 函數定義和通過 ASCII 字符串定義切片常量
* `s`—使用其內容（十六進制編碼並可選地進行位填充）定義原始切片常量
* `a`—從指定的地址創建包含 `MsgAddressInt` 結構的切片常量
* `u`—創建與提供的 ASCII 字符串的十六進制值對應的整數常量
* `h`—創建一個整數常量，其值是字符串的 SHA256 哈希的前 32 位
* `H`—創建一個整數常量，其值是字符串的 SHA256 哈希的全部 256 位
* `c`—創建一個整數常量，其值是字符串的 crc32 值


例如，以下值將導致相應的常量：
* `"string"` 變成 `x{737472696e67}` 切片常量
* `"abcdef"s` 變成 `x{abcdef}` 切片常量
* `"Ef8zMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM0vF"a` 變成 `x{9FE6666666666666666666666666666666666666666666666666666666666666667_}` 切片常量 (`addr_std$10 anycast:none$0 workchain_id:int8=0xFF address:bits256=0x33...33`)
* `"NstK"u` 變成 `0x4e73744b` 整數常量
* `"transfer(slice, int)"h` 變成 `0x7a62e8a8` 整數常量
* `"transfer(slice, int)"H` 變成 `0x7a62e8a8ebac41bd6de16c65e7be363bc2d2cbc6a0873778dead4795c13db979` 整數常量
* `"transfer(slice, int)"c` 變成 `2235694568` 整數常量


## 識別符
FunC 允許一個非常廣泛的識別符 (函數和變量名稱)。也就是說，任何不包含特殊符號 `;`, `,`, `(`, `)`, ` `（空格或制表符), `~` 和 `.`，不以注釋或字符串文字開頭 (用 `"`)，不是數字文字，不是下劃線 `_` 且不是關鍵字的 (單行) 字符串都是一個有效的識別符（唯一的例外是，如果它以 `` ` `` 開頭，它必須以相同的 `` ` `` 結尾，不能包含除了這兩個之外的任何其他 `` ` ``）。

此外，在函數定義中的函數名稱可以以 `.` 或 `~` 開頭。


例如，以下是有效的識別符：
- `query`，`query'`，`query''`
- `elem0`，`elem1`，`elem2`
- `CHECK`
- `_internal_value`
- `message_found?`
- `get_pubkeys&signatures`
- `dict::udict_set_builder`
- `_+_` (前綴表示法中的標準加法運算符，類型為 `(int, int) -> int`，但已經被定義)
- `fatal!`


當引入舊值的某個修改版本時，變量名稱末尾的 `'` 通常用於慣例。例如，幾乎所有用於 hashmap 操作的修改內置原始機制（除了帶有前綴 `~` 的內置原始機制）都需要一個 hashmap，並返回 hashmap 的新版本以及必要時的其他數據。將這些值命名為具有相同名稱的帶 `'` 的後綴名稱是很方便的。

後綴 `?` 通常用於布爾變量（TVM 沒有內置的布爾類型；布爾由整數表示：0 表示 false，-1 表示 true）或用於返回某些標誌的函數，通常表示操作的成功（例如來自 [stdlib.fc](/develop/func/stdlib) 的 `udict_get?`）。

以下是無效的識別符：
- `take(first)Entry`
- `"not_a_string`
- `msg.sender`
- `send_message,then_terminate`
- `_`

一些不常見的有效識別符示例：
- `123validname`
- `2+2=2*2`
- `-alsovalidname`
- `0xefefefhahaha`
- `{hehehe}`
- ``pa{--}in"`aaa`"``

以下也是無效的識別符：
- ``pa;;in"`aaa`"``（因為 `;` 被禁止了）
- `{-aaa-}`
- `aa(bb`
- `123`（它是一個數字）


此外，FunC 還有一種特殊的識別符類型，其在反引號 `` ` `` 中引用。
在引號中，任何符號都可以，除了 `\n` 和引號本身。

例如，`` `I'm a variable too` `` 是一個有效的識別符，以及 `` `any symbols ; ~ () are allowed here...` ``

## 常量
FunC 允許定義編譯時常量，這些常量在編譯期間進行替換和預計算。

常量定義為 `const optional-type identifier = value-or-expression;`

`optional-type` 可以用於強制常量的特定類型以及更好的可讀性。


現在支持 `int` 和 `slice` 類型。

`value-or-expression` 可以是文字或文字和常量的可預先計算的表達式。


例如，可以定義常量如下：
* `const int101 = 101;` 定義等於數字字面值 `101` 的 `int101` 常量。
* `const str1 = "const1", str2 = "aabbcc"s;` 定義兩個常量，它們等於它們對應的字符串。
* `const int int240 = ((int1 + int2) * 10) << 3;` 定義等於計算結果的 `int240` 常量。
* `const slice str2r = str2;` 定義等於 `str2` 常量值的 `str2r` 常量。


Since numeric constants are substituted during compilation, all optimization and pre-computations performed during the compilation are successfully performed (unlike the old method of defining constants via inline asm `PUSHINT`s).

由於數值常量在編譯期間被替換，因此在編譯期間執行的所有優化和預計算都能成功進行（這與通過內嵌 ASM `PUSHINT` 定義常量的舊方法不同）。