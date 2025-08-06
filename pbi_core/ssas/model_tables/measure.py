import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasRenameTable, SsasTable

from .column import Column

if TYPE_CHECKING:
    from .calc_dependency import CalcDependency
    from .kpi import KPI
    from .table import Table


class Measure(SsasRenameTable):
    data_category: str | None = None
    data_type: int
    description: str | None = None
    display_folder: str | None = None
    error_message: str | None = None
    expression: str | int | float | None = None
    format_string: str | int | None = None
    is_hidden: bool
    is_simple_measure: bool
    kpi_id: int | None = None
    lineage_tag: UUID
    name: str
    state: int
    table_id: int

    modified_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def KPI(self) -> Optional["KPI"]:  # noqa: N802
        if self.kpi_id is not None:
            return self.tabular_model.kpis.find({"id": self.kpi_id})
        return None

    def table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.table_id})

    def full_name(self) -> str:
        """Returns the fully qualified name for DAX queries."""
        table_name = self.table().name
        return f"'{table_name}'[{self.name}]"

    def data(self, columns: Column | list[Column], head: int = 100) -> list[dict[str, int | float | str]]:
        if isinstance(columns, Column):
            columns = [columns]
        column_str = "\n".join(
            col.full_name() + "," for col in columns
        )  # this should eventually be converted to jinja imo
        command = f"""
        EVALUATE TOPN({head}, SUMMARIZECOLUMNS(
            {column_str}
            {columns[0].table().name},
            "measure", {self.full_name()}
        ))
        """
        return self.tabular_model.server.query_dax(command)

    def __repr__(self) -> str:
        return f"Measure({self.table().name}.{self.name})"

    def child_measures(self) -> list["Measure"]:
        dependent_measures = self.tabular_model.calc_dependencies.find_all({
            "referenced_object_type": "MEASURE",
            "referenced_table": self.table().name,
            "referenced_object": self.name,
            "object_type": "MEASURE",
        })
        child_keys: list[tuple[str | None, str]] = [(m.table, m.object) for m in dependent_measures]
        full_dependencies = [m for m in self.tabular_model.measures if (m.table().name, m.name) in child_keys]
        return [x for x in full_dependencies if f"[{self.name}]" in str(x.expression)]

    def parent_measures(self) -> list["Measure"]:
        """Calculated columns can use Measures too :(."""
        dependent_measures: list[CalcDependency] = self.tabular_model.calc_dependencies.find_all({
            "object_type": "MEASURE",
            "table": self.table().name,
            "object": self.name,
            "referenced_object_type": "MEASURE",
        })
        parent_keys = [(m.referenced_table, m.referenced_object) for m in dependent_measures]
        full_dependencies = [m for m in self.tabular_model.measures if (m.table().name, m.name) in parent_keys]
        return [x for x in full_dependencies if f"[{x.name}]" in str(self.expression)]

    def child_columns(self) -> list["Column"]:
        """Only occurs when the dependent column is calculated (expression is not None)."""
        dependent_measures = self.tabular_model.calc_dependencies.find_all({
            "referenced_object_type": "MEASURE",
            "referenced_table": self.table().name,
            "referenced_object": self.name,
        })
        child_keys = [(m.table, m.object) for m in dependent_measures if m.object_type in {"CALC_COLUMN", "COLUMN"}]
        full_dependencies = [m for m in self.tabular_model.columns if (m.table().name, m.explicit_name) in child_keys]
        return [x for x in full_dependencies if f"[{self.name}]" in str(x.expression)]

    def parent_columns(self) -> list["Column"]:
        """Only occurs when column is calculated."""
        dependent_measures = self.tabular_model.calc_dependencies.find_all({
            "object_type": "MEASURE",
            "table": self.table().name,
            "object": self.name,
        })
        parent_keys = {
            (m.referenced_table, m.referenced_object)
            for m in dependent_measures
            if m.referenced_object_type in {"CALC_COLUMN", "COLUMN"}
        }
        full_dependencies = [c for c in self.tabular_model.columns if (c.table().name, c.explicit_name) in parent_keys]
        return [x for x in full_dependencies if f"[{x.explicit_name}]" in str(self.expression)]

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(
                self,
                lineage_type,
                [c.get_lineage(lineage_type) for c in self.child_measures() + self.child_columns()],
            )
        parent_nodes: list[SsasTable | None] = [
            self.KPI(),
            self.table(),
            *self.parent_measures(),
            *self.parent_columns(),
        ]
        parent_lineage = [c.get_lineage(lineage_type) for c in parent_nodes if c is not None]
        return LineageNode(self, lineage_type, parent_lineage)
