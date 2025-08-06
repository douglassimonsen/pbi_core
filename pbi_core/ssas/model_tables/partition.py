import datetime
from enum import IntEnum
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.logging import get_logger
from pbi_core.ssas.server.tabular_model import RefreshType, SsasRefreshRecord, SsasTable

from ._group import RowNotFoundError
from .column import Column

if TYPE_CHECKING:
    from collections.abc import Iterable

    from .query_group import QueryGroup
    from .table import Table


logger = get_logger()


class PartitionMode(IntEnum):
    """Source: https://learn.microsoft.com/en-us/analysis-services/tmsl/partitions-object-tmsl?view=asallproducts-allversions."""

    Import = 0
    DirectQuery = 1  # not verified
    default = 2  # not verified


class PartitionType(IntEnum):
    """Source: https://learn.microsoft.com/en-us/analysis-services/tmsl/partitions-object-tmsl?view=asallproducts-allversions."""

    NA = 1  # not verified
    Calculated = 2  # not verified
    Query = 4  # not verified


class Partition(SsasRefreshRecord):
    """Partitions are a child of Tables. They contain the Power Query code.

    Data refreshes occur on the Partition-level.

    SSAS spec: https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/81badb81-31a8-482b-ae16-5fc9d8291d9e
    """

    _default_refresh_typ = RefreshType.Full

    data_view: int
    data_source_id: int | None = None
    mode: PartitionMode
    name: str
    partition_storage_id: int
    query_definition: str
    query_group_id: int | None = None
    range_granularity: int
    retain_data_till_force_calculate: bool
    state: int
    system_flags: int
    table_id: int
    type: PartitionType

    modified_time: datetime.datetime
    refreshed_time: datetime.datetime

    def query_group(self) -> "QueryGroup | None":
        try:
            return self.tabular_model.query_groups.find({"id": self.table_id})
        except RowNotFoundError:
            return None

    def table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.table_id})

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        parent_nodes: list[SsasTable | None] = [self.table(), self.query_group()]
        parent_lineage: list[LineageNode] = [c.get_lineage(lineage_type) for c in parent_nodes if c is not None]
        return LineageNode(self, lineage_type, parent_lineage)

    def remove_columns(self, dropped_columns: "Iterable[Column | str | None]") -> BeautifulSoup:
        def pq_escape(x: str) -> str:
            """Beginning of column escaping for power query."""
            return x.replace('"', '""')

        """Adds a Table.RemoveColumns statement to the end of the Partition's PowerQuery.

        This means the upon refresh, the columns will not be included in the table
        """
        new_dropped_columns = []
        for col in dropped_columns:
            if isinstance(col, Column):
                # Tables have a column named "RowNumber-<UUID>" that cannot be removed in the PowerQuery
                if col._column_type() != "CALC_COLUMN" and not col.is_key:
                    new_dropped_columns.append(col.explicit_name)
            elif isinstance(col, str):
                new_dropped_columns.append(col)

        # TODO: create a powerquery parser to do this robustly
        new_dropped_columns = [pq_escape(x) for x in new_dropped_columns]
        logger.info("Updating partition to drop columns", table=self.table().name, columns=new_dropped_columns)
        lines = self.query_definition.split("\n")
        final_table_name = lines[-1].strip()
        setup = "\n".join(lines[:-2])

        prior_updates = setup.count("pbi_update")  # used to keep statement variables unique when applied multiple times
        new_final_table_name = f"pbi_update{prior_updates}"

        cols = ", ".join(f'"{x}"' for x in new_dropped_columns)
        setup += f",\n    {new_final_table_name} = Table.RemoveColumns({final_table_name}, {{{cols}}})"
        setup += f"\nin\n    {new_final_table_name}"
        self.query_definition = setup
        return self.alter()
