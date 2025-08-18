```mermaid
---
title: ColumnProperty
---
graph 
2430552678256["ColumnProperty"]
2430514799136["ProjectionConfig"]
2430514810848["Display"]
2430514805968["VCProperties"]
style 2430514805968 stroke:#ff0000,stroke-width:1px
2430071951472["PrototypeQuery"]
style 2430071951472 stroke:#ff0000,stroke-width:1px
2430514817680["QueryOptions"]
2430552678256 ---> 2430514805968
2430552678256 ---> 2430071951472
2430552678256 --->|display| 2430514810848
2430552678256 --->|queryOptions| 2430514817680
2430552678256 --->|projections| 2430514799136
```