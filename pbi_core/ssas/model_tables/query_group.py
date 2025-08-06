from typing import TYPE_CHECKING, Optional

from ...lineage import LineageNode, LineageType
from ..server.tabular_model import SsasBaseTable

if TYPE_CHECKING:
    from .expression import Expression
    from .model import Model
    from .partition import Partition


class QueryGroup(SsasBaseTable):
    description: Optional[str] = None
    folder: str
    model_id: int

    def expressions(self) -> list["Expression"]:
        return self.tabular_model.expressions.find_all({"query_group_id": self.id})

    def partitions(self) -> list["Partition"]:
        return self.tabular_model.partitions.find_all({"query_group_id": self.id})

    def model(self) -> "Model":
        return self.tabular_model.model

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(
                self,
                lineage_type,
                [expression.get_lineage(lineage_type) for expression in self.expressions()]
                + [partition.get_lineage(lineage_type) for partition in self.partitions()],
            )
        else:
            return LineageNode(self, lineage_type, [self.model().get_lineage(lineage_type)])
