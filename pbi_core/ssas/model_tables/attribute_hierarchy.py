import datetime
from typing import TYPE_CHECKING

from ...lineage import LineageNode
from ..server.tabular_model import SsasReadonlyTable

if TYPE_CHECKING:
    from .column import Column


class AttributeHierarchy(SsasReadonlyTable):
    attribute_hierarchy_storage_id: int
    column_id: int
    state: int

    modified_time: datetime.datetime
    refreshed_time: datetime.datetime

    def column(self) -> "Column":
        return self.tabular_model.columns.find({"id": self.column_id})

    def get_lineage(self) -> LineageNode:
        return LineageNode(self, [self.column().get_lineage()])
