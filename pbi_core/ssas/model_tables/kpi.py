import datetime
from typing import TYPE_CHECKING

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasBaseTable

if TYPE_CHECKING:
    from .measure import Measure


class KPI(SsasBaseTable):
    measure_id: int
    status_expression: str
    status_graphic: str
    target_expression: str
    target_format_string: str

    modified_time: datetime.datetime

    def pbi_core_name(self) -> str:
        return self.measure().pbi_core_name()

    def measure(self) -> "Measure":
        return self.tabular_model.measures.find({"id": self.measure_id})

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        return LineageNode(self, lineage_type, [self.measure().get_lineage(lineage_type)])
