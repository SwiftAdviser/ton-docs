# 註釋
FunC 有以 `;;` （雙 `;` ）開頭的單行註釋。例如：
```func
int x = 1; ;; assign 1 to x
```

FunC 也有以 `{-` 開頭，以 `-}` 結尾的多行註釋。請注意，與許多其他語言不同，FunC 的多行註釋可以嵌套。例如：
```func
{- This is a multi-line comment
    {- this is a comment in the comment -}
-}
```

此外，在多行註釋中還可以有單行註釋，且單行註釋 `;;` 的優先權高於多行註釋 `{- -}` 。換句話說，在以下示例中：

```func
{-
  Start of the comment

;; this comment ending is itself commented -> -}

const a = 10;
;; this comment begining is itself commented -> {-

  End of the comment
-}
```

`const a = 10;` 被嵌在多行註釋中，被注釋掉了。