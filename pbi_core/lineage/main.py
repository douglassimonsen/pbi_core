from typing import Any, Optional


class LineageNode:
    value: Any
    parents: list["LineageNode"] = []

    def __init__(self, value: Any, parents: Optional[list["LineageNode"]] = None) -> None:
        self.value = value
        self.parents = parents or []

    def to_mermaid(self) -> None:
        raise NotImplementedError
