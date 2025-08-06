import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from ...lineage import LineageNode
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

    def get_lineage(self, children: bool = False, parents: bool = True) -> LineageNode:
        return LineageNode(self, [self.column().get_lineage(), self.hierarchy().get_lineage()])
