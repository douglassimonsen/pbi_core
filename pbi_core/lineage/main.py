from typing import Any, Literal, Optional

from python_mermaid.diagram import Link, MermaidDiagram, Node

LineageType = Literal["children"] | Literal["parents"]


class LineageNode:
    value: Any
    relatives: list["LineageNode"]
    lineage_type: LineageType

    def __init__(self, value: Any, lineage_type: LineageType, relatives: Optional[list["LineageNode"]] = None) -> None:
        self.value = value
        self.relatives = relatives or []
        self.lineage_type = lineage_type

    def _to_mermaid_helper(self):
        pass

    def to_mermaid(self) -> MermaidDiagram:
        nodes = [
            Node(
                id=f"{self.value.__class__.__name__}-{self.value.id}",
            )
        ]
        links = []
        for relative in self.relatives:
            child_node = Node(id=f"{relative.value.__class__.__name__}-{relative.value.id}")
            links.append(Link(nodes[0], child_node))
            nodes.append(child_node)

        return MermaidDiagram(title="Lineage Chart", nodes=nodes, links=links)
