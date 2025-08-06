import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from ...lineage import LineageNode, LineageType
from ..server.tabular_model import SsasRenameTable

if TYPE_CHECKING:
    from .column import Column
    from .hierarchy import Hierarchy


class Level(SsasRenameTable):
    column_id: int
    hierarchy_id: int
    lineage_tag: UUID
    name: str
    ordinal: int

    modified_time: datetime.datetime

    def column(self) -> "Column":
        return self.tabular_model.columns.find({"id": self.column_id})

    def hierarchy(self) -> "Hierarchy":
        return self.tabular_model.hierarchies.find({"id": self.hierarchy_id})

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        else:
            return LineageNode(
                self,
                lineage_type,
                [self.column().get_lineage(lineage_type), self.hierarchy().get_lineage(lineage_type)],
            )
