from typing import Any, Literal, Optional

LineageType = Literal["children"] | Literal["parents"]


class LineageNode:
    value: Any
    relatives: list["LineageNode"]
    lineage_type: LineageType

    def __init__(self, value: Any, lineage_type: LineageType, relatives: Optional[list["LineageNode"]] = None) -> None:
        self.value = value
        self.relatives = relatives or []
        self.lineage_type = lineage_type

    def to_mermaid(self) -> None:
        raise NotImplementedError
