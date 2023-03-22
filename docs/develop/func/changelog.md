# FunC 的歷史

## 初始版本
初始版本由 Telegram 完成，在 2020 年 5 月後停止了積極開發。我們將 2020 年 5 月版本稱為“初始版本”。

## 版本 0.1.0
於 [05.2022 更新](https://github.com/ton-blockchain/ton/releases/tag/v2022.05) 中發佈。

在此版本中新增了：
- [常數](/develop/func/literals_identifiers#constants)
- [擴展字串文字](/develop/func/literals_identifiers#string-literals)
- [Semver pragma](/develop/func/compiler_directives#pragma-version)
- [Include](/develop/func/compiler_directives#pragma-version)

修正：
- 修正了 Asm.fif 中很少發生的錯誤。



## 版本 0.2.0
於 [08.2022 更新](https://github.com/ton-blockchain/ton/releases/tag/v2022.08) 中發佈。

在此版本中新增了：
- 不平衡的 if/else 分支（當某些分支返回而某些分支不返回時）

修正：
- [FunC 不正確處理 while(false) 迴圈 #377](https://github.com/ton-blockchain/ton/issues/377)
- [FunC 不正確生成 ifelse 分支的程式碼 #374](https://github.com/ton-blockchain/ton/issues/374)
- [FunC 在內聯函數中不正確返回條件 #370](https://github.com/ton-blockchain/ton/issues/370)
- [Asm.fif：將大型函數體拆分不正確地干擾了內聯函數 #375](https://github.com/ton-blockchain/ton/issues/375)


## 版本 0.3.0
於 [10.2022 更新](https://github.com/ton-blockchain/ton/releases/tag/v2022.10) 中發佈。

在此版本中新增了：
- [多行組合語言指令](/develop/func/functions#multiline-asms)
- 允許複製相同定義的常數和組合語言指令
- 允許對常數進行位元運算

## 版本 0.4.0
於 [01.2023 更新](https://github.com/ton-blockchain/ton/releases/tag/v2023.01) 中發佈。

在此版本中新增了：
- [try/catch 陳述式](/develop/func/statements#try-catch-statements)
- [throw_arg 函數](/develop/func/builtins#throwing-exceptions)
- 允許原地修改和大量分配全局變數：`a~inc()` 和 `(a, b) = (3, 5)`，其中 `a` 是全局變數

修正：
- 禁止在同一表達式中使用後修改本地變數的歧義修改：`var x = (ds, ds~load_uint(32), ds~load_unit(64));` 被禁止，而 `var x = (ds~load_uint(32), ds~load_unit(64), ds);` 則未被禁止。
- 允許空的內聯函數
- 修正罕見的 `while` 優化錯誤。
