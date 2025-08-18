```mermaid
---
title: LinearGradient2Expression
---
graph 
2430071896816["SolidExpression"]
style 2430071896816 stroke:#ff0000,stroke-width:1px
2430071906576["LinearGradient2Helper"]
2430071816784["LiteralSource"]
style 2430071816784 stroke:#ff0000,stroke-width:1px
2430071920240["LinearGradient2Expression"]
2430071909504["StrategyExpression"]
2430071887056["LiteralExpression"]
style 2430071887056 stroke:#ff0000,stroke-width:1px
2430071920240 --->|linearGradient2| 2430071906576
2430071909504 ---> 2430071887056
2430071906576 --->|nullColoringStrategy| 2430071909504
2430071906576 ---> 2430071896816
2430071909504 ---> 2430071816784
```