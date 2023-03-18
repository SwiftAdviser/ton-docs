# IDE Support


### Highlight
The [intellij-ton](https://github.com/andreypfau/intellij-ton) plugin supports Fift, FunC and also TL-B.  
The TL-B grammar is described in the [TlbParser.bnf](https://github.com/andreypfau/intellij-ton/blob/main/src/main/grammars/TlbParser.bnf) file.

### TL-B Parsers

TL-B parsers helps to serialize basic structures. Each of them implements TL-B structures as object, and returns serialized binary data.

| language/stack | SDK                                                                             | social                  |
|----------------|---------------------------------------------------------------------------------|-------------------------|
| Kotlin         | [ton-kotlin](https://github.com/andreypfau/ton-kotlin/tree/main/ton-kotlin-tlb) | https://t.me/tonkotlin  |
| Go             | [tonutils](https://github.com/xssnick/tonutils-go/tree/master/tlb)              | https://t.me/tonutils   |
| TypeScript     | [tlb-parser](https://github.com/ton-community/tlb-parser)                       | -|
