```mermaid
---
title: ScopedEvalArith
---
graph 
2430071365824["ColumnSource"]
style 2430071365824 stroke:#ff0000,stroke-width:1px
2430071359968["MeasureSource"]
style 2430071359968 stroke:#ff0000,stroke-width:1px
2430071371680["ScopedEvalAgg"]
style 2430071371680 stroke:#ff0000,stroke-width:1px
2430071361920["ScopedEval2"]
2430071358016["AggregationSource"]
style 2430071358016 stroke:#ff0000,stroke-width:1px
2430071376560["ScopedEvalArith"]
2430071363872["HierarchyLevelSource"]
style 2430071363872 stroke:#ff0000,stroke-width:1px
2430071360944["AllRolesRef"]
2430071376560 --->|ScopedEval| 2430071361920
2430071361920 ---> 2430071371680
2430071361920 ---> 2430071365824
2430071361920 ---> 2430071359968
2430071361920 ---> 2430071363872
2430071361920 ---> 2430071358016
2430071361920 --->|Scope| 2430071360944
```