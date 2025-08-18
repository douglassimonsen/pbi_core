```mermaid
---
title: ConditionalSource
---
graph 
2430071900720["ConditionalCase"]
2430071874368["ComparisonCondition"]
style 2430071874368 stroke:#ff0000,stroke-width:1px
2430071903648["ConditionalSource"]
2430071846064["ContainsCondition"]
style 2430071846064 stroke:#ff0000,stroke-width:1px
2430071879248["OrCondition"]
style 2430071879248 stroke:#ff0000,stroke-width:1px
2430071816784["LiteralSource"]
style 2430071816784 stroke:#ff0000,stroke-width:1px
2430071880224["NotCondition"]
style 2430071880224 stroke:#ff0000,stroke-width:1px
2430071878272["ExistsCondition"]
style 2430071878272 stroke:#ff0000,stroke-width:1px
2430071893888["_ConditionalSourceHelper"]
2430071854848["InCondition"]
style 2430071854848 stroke:#ff0000,stroke-width:1px
2430071876320["AndCondition"]
style 2430071876320 stroke:#ff0000,stroke-width:1px
2430071900720 ---> 2430071816784
2430071900720 ---> 2430071846064
2430071900720 ---> 2430071876320
2430071900720 ---> 2430071854848
2430071900720 ---> 2430071878272
2430071900720 ---> 2430071874368
2430071900720 ---> 2430071880224
2430071893888 --->|Cases| 2430071900720
2430071903648 --->|Conditional| 2430071893888
2430071900720 ---> 2430071879248
```