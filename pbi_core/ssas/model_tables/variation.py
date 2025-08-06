from typing import TYPE_CHECKING, Any, Optional

from ..server.tabular_model import SsasTable

if TYPE_CHECKING:
    from .column import Column
    from .hierarchy import Hierarchy
    from .relationship import Relationship


class Variation(SsasTable):
    column: Optional[Any] = None
    column_id: int
    default_hierarchy_id: int
    is_default: bool
    name: str
    relationship_id: int

    def get_column(self) -> Optional["Column"]:
        """
        Name is bad to not shadow the column field in this entity :(
        """
        return self.tabular_model.columns.find({"id": self.column_id})

    def default_hierarchy(self) -> "Hierarchy":
        return self.tabular_model.hierarchies.find({"id": self.default_hierarchy_id})

    def relationship(self) -> "Relationship":
        return self.tabular_model.relationships.find({"id": self.relationship_id})
