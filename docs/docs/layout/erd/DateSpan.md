```mermaid
---
title: DateSpan
---
graph 
2430071851920["_DateSpanHelper"]
2430071852896["DateSpan"]
2430071856800["_NowHelper"]
2430071816784["LiteralSource"]
style 2430071816784 stroke:#ff0000,stroke-width:1px
2430071851920 ---> 2430071816784
2430071851920 --->|Expression| 2430071856800
2430071852896 --->|DateSpan| 2430071851920
```