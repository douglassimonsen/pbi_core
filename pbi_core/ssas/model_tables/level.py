import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from ..server.tabular_model import SsasTable

if TYPE_CHECKING:
    from .column import Column
    from .hierarchy import Hierarchy


class Level(SsasTable):
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
