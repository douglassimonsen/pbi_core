import datetime
from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from ...lineage import LineageNode, LineageType
from ..server.tabular_model import SsasRefreshTable, SsasTable
from ._group import RowNotFoundError

if TYPE_CHECKING:
    from .query_group import QueryGroup
    from .table import Table


class PartitionMode(IntEnum):
    """
    Source: https://learn.microsoft.com/en-us/analysis-services/tmsl/partitions-object-tmsl?view=asallproducts-allversions
    """

    Import = 0
    DirectQuery = 1  # not verified
    default = 2  # not verified


class PartitionType(IntEnum):
    """
    Source: https://learn.microsoft.com/en-us/analysis-services/tmsl/partitions-object-tmsl?view=asallproducts-allversions
    """

    Calculated = 2  # not verified
    Query = 4  # not verified


class Partition(SsasRefreshTable):
    """Partitions are a child of Tables. They contain the Power Query code. Data refreshes occur on the Partition-level"""

    data_view: int
    mode: PartitionMode
    name: str
    partition_storage_id: int
    query_definition: str
    query_group_id: Optional[int] = None
    range_granularity: int
    retain_data_till_force_calculate: bool
    state: int
    system_flags: int
    table_id: int
    type: PartitionType

    modified_time: datetime.datetime
    refreshed_time: datetime.datetime

    def query_group(self) -> Optional["QueryGroup"]:
        try:
            return self.tabular_model.query_groups.find({"id": self.table_id})
        except RowNotFoundError:
            return None

    def table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.table_id})

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        else:
            parent_nodes: list[Optional[SsasTable]] = [self.table(), self.query_group()]
            parent_lineage: list[LineageNode] = [c.get_lineage(lineage_type) for c in parent_nodes if c is not None]
            return LineageNode(self, lineage_type, parent_lineage)
