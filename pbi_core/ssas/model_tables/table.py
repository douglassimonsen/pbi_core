import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from ...lineage import LineageNode, LineageType
from ..server.tabular_model import SsasRefreshTable
from .column import Column
from .measure import Measure
from .partition import Partition

if TYPE_CHECKING:
    from .model import Model


class Table(SsasRefreshTable):
    alternate_source_precedence: int
    data_category: Optional[str] = None
    description: Optional[str] = None
    exclude_from_model_refresh: bool
    is_hidden: bool
    is_private: bool
    lineage_tag: UUID
    model_id: int
    name: str
    show_as_variations_only: bool
    system_flags: int
    system_managed: Optional[bool] = None
    table_storage_id: Optional[int] = None

    modified_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def data(self, head: int = 100) -> list[int | float | str]:
        ret = self.tabular_model.server.query_dax(
            f"EVALUATE TOPN({head}, ALL('{self.name}'))",
            db_name=self.tabular_model.db_name,
        )
        return [next(iter(row.values())) for row in ret]

    def partitions(self) -> list[Partition]:
        return self.tabular_model.partitions.find_all({"table_id": self.id})

    def columns(self) -> list[Column]:
        return self.tabular_model.columns.find_all({"table_id": self.id})

    def measures(self) -> list[Measure]:
        return self.tabular_model.measures.find_all({"table_id": self.id})

    def model(self) -> "Model":
        return self.tabular_model.model

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(
                self,
                lineage_type,
                [col.get_lineage(lineage_type) for col in self.columns()]
                + [partition.get_lineage(lineage_type) for partition in self.partitions()]
                + [measure.get_lineage(lineage_type) for measure in self.measures()],
            )
        else:
            return LineageNode(self, lineage_type, [self.model().get_lineage(lineage_type)])
