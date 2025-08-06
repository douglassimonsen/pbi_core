import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from ..server.tabular_model import SsasRenameTable, SsasTable

if TYPE_CHECKING:
    from .model import Model
    from .query_group import QueryGroup
from ...lineage import LineageNode


class Expression(SsasRenameTable):
    description: Optional[str] = None
    expression: str
    kind: int
    lineage_tag: UUID
    model_id: int
    name: str
    query_group_id: Optional[int] = None

    modified_time: datetime.datetime

    def model(self) -> "Model":
        return self.tabular_model.model

    def query_group(self) -> Optional["QueryGroup"]:
        return self.tabular_model.query_groups.find({"id": self.query_group_id})

    def get_lineage(self, children: bool = False, parents: bool = True) -> LineageNode:
        parent_nodes: list[Optional[SsasTable]] = [self.model(), self.query_group()]
        parent_lineage = [p.get_lineage() for p in parent_nodes if p is not None]
        return LineageNode(self, parent_lineage)
