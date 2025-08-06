import datetime
from typing import TYPE_CHECKING

from ...lineage import LineageNode
from ..server.tabular_model import SsasBaseTable

if TYPE_CHECKING:
    from .measure import Measure


class KPI(SsasBaseTable):
    measure_id: int
    status_expression: str
    status_graphic: str
    target_expression: str
    target_format_string: str

    modified_time: datetime.datetime

    def measure(self) -> "Measure":
        return self.tabular_model.measures.find({"id": self.measure_id})

    def get_lineage(self, children: bool = False, parents: bool = True) -> LineageNode:
        return LineageNode(self, [self.measure().get_lineage()])
