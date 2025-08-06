import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pbi_core.ssas.server.tabular_model import SsasRenameRecord, SsasTable

if TYPE_CHECKING:
    from .model import Model
    from .query_group import QueryGroup
from pbi_core.lineage import LineageNode, LineageType


class Expression(SsasRenameRecord):
    description: str | None = None
    expression: str
    kind: int
    lineage_tag: UUID = uuid4()
    model_id: int
    name: str
    query_group_id: int | None = None

    modified_time: datetime.datetime

    def model(self) -> "Model":
        return self.tabular_model.model

    def query_group(self) -> "QueryGroup | None":
        return self.tabular_model.query_groups.find({"id": self.query_group_id})

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        parent_nodes: list[SsasTable | None] = [self.model(), self.query_group()]
        parent_lineage = [p.get_lineage(lineage_type) for p in parent_nodes if p is not None]
        return LineageNode(self, lineage_type, parent_lineage)
