from typing import Any, Literal, Optional

from mermaid import Link, MermaidDiagram, Node
from mermaid.node import NodeShape

LineageType = Literal["children"] | Literal["parents"]


"""
#ffffcc, #ffcc99, #ffcccc,
#ff99cc, #ffccff, #cc99ff,
#ccccff, #99ccff, #ccffff,
#99ffcc, #ccffcc, #ccff99,
"""

CLASS_STYLES = {
    "AttributeHierarchy": "fill:#ffffcc,stroke:#333,stroke-width:1px",
    "Column": "fill:#ffcc99,stroke:#333,stroke-width:1px",
    "Culture": "fill:#ffcccc,stroke:#333,stroke-width:1px",
    "LinguisticMetadata": "fill:#ff99cc,stroke:#333,stroke-width:1px",
    "Measure": "fill:#ffccff,stroke:#333,stroke-width:1px",
    "Table": "fill:#cc99ff,stroke:#333,stroke-width:1px",
}


class LineageNode:
    value: Any
    relatives: list["LineageNode"]
    lineage_type: LineageType

    def __init__(self, value: Any, lineage_type: LineageType, relatives: Optional[list["LineageNode"]] = None) -> None:
        self.value = value
        self.relatives = relatives or []
        self.lineage_type = lineage_type

    def _to_mermaid_helper(self, node: Node) -> tuple[list[Node], list[Link]]:
        nodes = [node]
        links = []
        for relative in self.relatives:
            child_node = Node(
                id=f"{relative.value.__class__.__name__}-{relative.value.id}",
                style=CLASS_STYLES[relative.value.__class__.__name__],
                shape=NodeShape.round_edge,
            )
            child_nodes, child_links = relative._to_mermaid_helper(child_node)
            links.append(Link(nodes[0], child_node))
            links.extend(child_links)
            nodes.extend(child_nodes)
        return nodes, links

    def to_mermaid(self) -> MermaidDiagram:
        base_node = Node(
            id=f"{self.value.__class__.__name__}-{self.value.id}",
        )
        nodes, links = self._to_mermaid_helper(base_node)

        return MermaidDiagram(title="Lineage Chart", nodes=nodes, links=links)
