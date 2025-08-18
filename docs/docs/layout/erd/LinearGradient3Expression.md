```mermaid
---
title: LinearGradient3Expression
---
graph 
2430071914384["LinearGradient3Helper"]
2430071896816["SolidExpression"]
style 2430071896816 stroke:#ff0000,stroke-width:1px
2430071816784["LiteralSource"]
style 2430071816784 stroke:#ff0000,stroke-width:1px
2430071909504["StrategyExpression"]
2430071887056["LiteralExpression"]
style 2430071887056 stroke:#ff0000,stroke-width:1px
2430071910480["LinearGradient3Expression"]
2430071914384 --->|nullColoringStrategy| 2430071909504
2430071910480 --->|linearGradient3| 2430071914384
2430071909504 ---> 2430071887056
2430071909504 ---> 2430071816784
2430071914384 ---> 2430071896816
```