```mermaid
---
title: ImageKindExpression
---
graph 
2430071903648["ConditionalSource"]
style 2430071903648 stroke:#ff0000,stroke-width:1px
2430071926096["ImageKindExpression"]
2430071887056["LiteralExpression"]
style 2430071887056 stroke:#ff0000,stroke-width:1px
2430071908528["ConditionalExpression"]
2430071926096 --->|value| 2430071908528
2430071926096 ---> 2430071887056
2430071908528 ---> 2430071903648
```