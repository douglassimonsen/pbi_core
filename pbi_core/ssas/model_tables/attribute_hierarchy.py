import datetime
from typing import TYPE_CHECKING

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasReadonlyRecord

if TYPE_CHECKING:
    from .column import Column
    from .level import Level


class AttributeHierarchy(SsasReadonlyRecord):
    attribute_hierarchy_storage_id: int
    column_id: int
    state: int

    modified_time: datetime.datetime
    refreshed_time: datetime.datetime

    def pbi_core_name(self) -> str:
        """Returns the name displayed in the PBIX report."""
        return self.column().pbi_core_name()

    def column(self) -> "Column":
        return self.tabular_model.columns.find({"id": self.column_id})

    def levels(self) -> set["Level"]:
        return self.tabular_model.levels.find_all({"hierarchy_id": self.id})

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type, [level.get_lineage(lineage_type) for level in self.levels()])
        return LineageNode(self, lineage_type, [self.column().get_lineage(lineage_type)])
