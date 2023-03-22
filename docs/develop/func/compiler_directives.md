# 編譯指令
這些關鍵字以 `#` 開頭，指示編譯器執行某些操作、檢查或更改參數。

這些指令只能在最外層級使用（不在任何函數定義內部）。

## #include
`#include` 指令允許包含另一個 FunC 源代碼文件，該文件將被解析並包含在此處。

語法是 `#include "filename.fc";`。文件會自動檢查是否重複包含，如果超過一次，將被忽略，如果詳細程度不低於2，則會發出警告。

如果在解析被包含的文件時發生錯誤，那麼還會打印出包含的堆棧，其中每個包含文件的位置都會被打印出來。


markdown
Copy code
## #pragma
`#pragma` 指令用於在語言本身無法傳達的情況下向編譯器提供其他信息。

### #pragma version
版本指令用於在編譯文件時強制執行特定版本的 FunC 編譯器。

版本以 semver 格式指定，即 _a.b.c_，其中 _a_ 是主版本，_b_ 是次要版本，_c_ 是修補程式。

開發人員可以使用幾種比較運算符：
* _a.b.c_ 或 _=a.b.c_——需要正確的 _a.b.c_ 版本的編譯器
* _>a.b.c_——需要編譯器版本高於 _a.b.c_，
  * _>=a.b.c_——需要編譯器版本高於或等於 _a.b.c_
* _<a.b.c_——需要編譯器版本低於 _a.b.c_，
  * _<=a.b.c_——需要編譯器版本低於或等於 _a.b.c_
* _^a.b.c_——要求主要編譯器版本等於“a”部分，次要版本不低於“b”部分，
  * _^a.b_——要求主要編譯器版本等於 _a_ 部分，次要版本不低於 _b_ 部分
  * _^a_——要求主要編譯器版本不低於 _a_ 部分

其他比較運算符（_=，_>，_>=，_<，_<=）的短格式假定遺漏部分的值為零，即：
* _>a.b_ 等同於 _>a.b.0_（因此不匹配 _a.b.0_ 版本）
* _<=a_ 等同於 _<=a.0.0_（因此不匹配 _a.0.1_ 版本）
* _^a.b.0_ 與 _^a.b_ **不同**

例如，_^a.1.2_ 匹配 _a.1.3_，但不匹配 _a.2.3_ 或 _a.1.0_，但 _^a.1_ 可以匹配它們所有。

此指令可以多次使用；編譯器版本必須滿足所有提供的條件。

### #pragma not-version
此指令的語法與版本指令相同，但如果條件滿足，則失敗。

例如，可以用於黑名單特定版本已知存在問題。


### #pragma allow-post-modification
_funC v0.4.1_

默認情況下，在同一表達式中對變量進行修改前禁止使用它。換句話說，表達式`(x, y) = (ds, ds~load_uint(8))`不會被編譯，而`(x, y) = (ds~load_uint(8), ds)`則是有效的。

這個規則可以被覆蓋，通過`#pragma allow-post-modification`，允許在賦值和函數調用後修改變量；如常子表達式將從左到右計算：`(x, y) = (ds, ds~load_bits(8))`將導致`x`包含初始的`ds`；`f(ds, ds~load_bits(8))`的第一個參數將包含初始的`ds`，第二個參數將包含`ds`的 8 位。

`#pragma allow-post-modification`僅適用於該指令之後的代碼。


### #pragma compute-asm-ltr
_funC v0.4.1_

Asm 声明可以覆盖参数的顺序，例如在以下表达式中：


```func
idict_set_ref(ds~load_dict(), ds~load_uint(8), ds~load_uint(256), ds~load_ref())
```

由於以下 asm 声明（注意 `asm(value index dict key_len)`），解析的順序將為：`load_ref()`，`load_uint(256)`，`load_dict()` 和 `load_uint(8)`：


```func
cell idict_set_ref(cell dict, int key_len, int index, cell value) asm(value index dict key_len) "DICTISETREF";
```

透過 `#pragma compute-asm-ltr` 可以將此行為更改為嚴格的從左到右的計算順序。

因此，在以下代碼中：

```func
#pragma compute-asm-ltr
...
idict_set_ref(ds~load_dict(), ds~load_uint(8), ds~load_uint(256), ds~load_ref());
```
解析的順序將是 `load_dict()`，`load_uint(8)`，`load_uint(256)`，`load_ref()`，並且所有 asm 排列都會在計算之後發生。

`#pragma compute-asm-ltr` 只適用於 pragma 後的代碼。
