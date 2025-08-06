import datetime
from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from ..server.tabular_model import SsasRefreshTable

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
        return self.tabular_model.query_groups.find({"id": self.table_id})

    def table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.table_id})
