# 全局變量
FunC 程序本質上是函數聲明/定義和全局變量聲明的列表。本節將涵蓋第二個主題。

可以使用 `global` 關鍵字和變量類型以及變量名聲明全局變量。例如，

```func
global ((int, int) -> int) op;

int check_assoc(int a, int b, int c) {
  return op(op(a, b), c) == op(a, op(b, c));
}

int main() {
  op = _+_;
  return check_assoc(2, 3, 9);
}
```
這是一個簡單的程序，它將加法運算符 `_+_` 寫入全局函數變量 `op`，並檢查三個樣本整數的加法結合律; 2、3 和 9。

在內部，全局變量存儲在 TVM 的 c7 控制寄存器中。

全局變量的類型可以省略。如果省略，它將從變量的使用中推斷出來。例如，我們可以將程序重寫為：

```func
global op;

int check_assoc(int a, int b, int c) {
  return op(op(a, b), c) == op(a, op(b, c));
}

int main() {
  op = _+_;
  return check_assoc(2, 3, 9);
}
```

可以在同一個 `global` 關鍵字後聲明多個變量。以下代碼等價：

```func
global int A;
global cell B;
global C;
```
```func
global int A, cell B, C;
```

不允許聲明與已聲明的全局變量同名的本地變量。例如，此代碼不會編譯：
```func
global cell C;

int main() {
  int C = 3;
  return C;
}
```
注意，以下代碼是正確的：
```func
global int C;

int main() {
  int C = 3;
  return C;
}
```
但是在這裡 `int C = 3;` 等價於 `C = 3;`，即這是對全局變量 `C` 的賦值，而不是局部變量 `C` 的聲明（您可以在 [語句](/develop/func/statements#variable-declaration) 部分中找到有關此效果的說明）。
