# 註解
FunC 使用以 `;;`（兩個分號）開頭的單行註解。例如：
```func
int x = 1; ;; assign 1 to x
```

FunC 還有多行註解，它們以 `{-` 開始，以 `-}` 結束。請注意，與許多其他語言不同，FunC 的多行註解可以嵌套。例如：
```func
{- This is a multi-line comment
    {- this is a comment in the comment -}
-}
```

此外，在多行註解中可以有單行註解，而單行註解 `;;` 的"強度"優先於多行註解`{- -}`。換句話說，在以下示例中：

```func
{-
  Start of the comment

;; this comment ending is itself commented -> -}

const a = 10;
;; this comment begining is itself commented -> {-

  End of the comment
-}
```

`const a = 10;` 在多行註解中並被註解掉了。
