from typing import TYPE_CHECKING, Optional

from ..server.tabular_model import SsasTable
from ._base import SsasBaseCommands

if TYPE_CHECKING:
    from .expression import Expression
    from .partition import Partition


class QueryGroup(SsasTable):
    description: Optional[str] = None
    folder: str
    model_id: int
    _commands: SsasBaseCommands

    def expressions(self) -> list["Expression"]:
        return self.tabular_model.expressions.find_all({"query_group_id": self.id})

    def partitions(self) -> list["Partition"]:
        return self.tabular_model.partitions.find_all({"query_group_id": self.id})
