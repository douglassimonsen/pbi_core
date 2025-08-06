import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from ...lineage import LineageNode, LineageType
from ..server.tabular_model import SsasRenameTable, SsasTable
from .column import Column

if TYPE_CHECKING:
    from .kpi import KPI
    from .table import Table


class Measure(SsasRenameTable):
    data_category: Optional[str] = None
    data_type: int
    description: Optional[str] = None
    display_folder: Optional[str] = None
    error_message: Optional[str] = None
    expression: Optional[str | int | float] = None
    format_string: Optional[str | int] = None
    is_hidden: bool
    is_simple_measure: bool
    kpi_id: Optional[int] = None
    lineage_tag: UUID
    name: str
    state: int
    table_id: int

    modified_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def lineage_name(self) -> str:
        return self.name

    def KPI(self) -> Optional["KPI"]:
        if self.kpi_id is not None:
            return self.tabular_model.kpis.find({"id": self.kpi_id})

    def table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.table_id})

    def data(self, column: Column, head: int = 100) -> list[dict[str, int | float | str]]:
        column_name = column.full_name()
        ret = self.tabular_model.server.query_dax(
            f'EVALUATE TOPN({head}, ADDCOLUMNS(VALUES({column_name}), "measure", [{self.name}]))',
            db_name=self.tabular_model.db_name,
        )
        clean_name = column_name.replace("'", "")  # sure this will get more complicated lol
        return [
            {
                "column_value": x[clean_name],
                "measure_value": x["[measure]"],
            }
            for x in ret
        ]

    def __repr__(self) -> str:
        return f"Measure({self.table().name}.{self.name})"

    def child_measures(self) -> list["Measure"]:
        dependent_measures = self.tabular_model.calc_dependencies.find_all({
            "referenced_object_type": "MEASURE",
            "referenced_table": self.table().name,
            "referenced_object": self.name,
        })
        dependent_measure_keys = [(m.table, m.object) for m in dependent_measures]
        ret = [m for m in self.tabular_model.measures if (m.table().name, m.name) in dependent_measure_keys]
        return ret

    def parent_measures(self) -> list["Measure"]:
        return []

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type, [c.get_lineage(lineage_type) for c in self.child_measures()])
        else:
            parent_nodes: list[Optional[SsasTable]] = [self.KPI(), self.table()] + self.parent_measures()  # type: ignore
            parent_lineage = [c.get_lineage(lineage_type) for c in parent_nodes if c is not None]
            return LineageNode(self, lineage_type, parent_lineage)
