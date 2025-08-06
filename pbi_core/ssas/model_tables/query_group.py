from typing import TYPE_CHECKING, Optional

from ..server.tabular_model import SsasBaseTable

if TYPE_CHECKING:
    from .expression import Expression
    from .partition import Partition


class QueryGroup(SsasBaseTable):
    description: Optional[str] = None
    folder: str
    model_id: int

    def expressions(self) -> list["Expression"]:
        return self.tabular_model.expressions.find_all({"query_group_id": self.id})

    def partitions(self) -> list["Partition"]:
        return self.tabular_model.partitions.find_all({"query_group_id": self.id})
