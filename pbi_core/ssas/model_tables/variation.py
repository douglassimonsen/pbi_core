from typing import TYPE_CHECKING, Any

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasRenameTable

if TYPE_CHECKING:
    from .column import Column
    from .hierarchy import Hierarchy
    from .relationship import Relationship


class Variation(SsasRenameTable):
    column: Any | None = None
    column_id: int
    default_hierarchy_id: int
    is_default: bool
    name: str
    relationship_id: int

    def get_column(self) -> "Column | None":
        """Name is bad to not shadow the column field in this entity :(."""
        return self.tabular_model.columns.find({"id": self.column_id})

    def default_hierarchy(self) -> "Hierarchy":
        return self.tabular_model.hierarchies.find({"id": self.default_hierarchy_id})

    def relationship(self) -> "Relationship":
        return self.tabular_model.relationships.find({"id": self.relationship_id})

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        return LineageNode(
            self,
            lineage_type,
            [
                self.default_hierarchy().get_lineage(lineage_type),
                self.relationship().get_lineage(lineage_type),
            ],
        )
