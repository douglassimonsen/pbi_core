```mermaid
---
title: Pod
---
graph 
2430514895760["PodConfig"]
2430071365824["ColumnSource"]
style 2430071365824 stroke:#ff0000,stroke-width:1px
2430514896736["Pod"]
2430514885024["Parameter"]
2430514896736 --->|parameters| 2430514885024
2430514896736 --->|config| 2430514895760
2430514885024 ---> 2430071365824
```