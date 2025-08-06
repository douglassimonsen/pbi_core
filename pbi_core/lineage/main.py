from typing import Any


class LineageNode:
    value: Any
    children: list["LineageNode"] = []

    def __init__(self, value: Any, children: list["LineageNode"]) -> None:
        self.value = value
        self.children = children

    def to_mermaid(self) -> None:
        raise NotImplementedError
