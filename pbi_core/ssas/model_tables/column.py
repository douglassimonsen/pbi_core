import datetime
from typing import TYPE_CHECKING, ClassVar, Optional
from uuid import UUID

from ...lineage import LineageNode, LineageType
from ..server.tabular_model import SsasRenameTable, SsasTable

if TYPE_CHECKING:
    from .attribute_hierarchy import AttributeHierarchy
    from .level import Level
    from .measure import Measure
    from .relationship import Relationship
    from .table import Table


class Column(SsasRenameTable):
    _field_mapping: ClassVar[dict[str, str]] = {
        "description": "Description",
    }
    _db_name_field: str = "ExplicitName"
    _read_only_fields = ("table_id",)

    alignment: int
    attribute_hierarchy_id: int
    column_origin_id: Optional[int] = None
    column_storage_id: int
    data_category: Optional[str] = None
    description: Optional[str] = None
    display_folder: Optional[str] = None
    display_ordinal: int
    encoding_hint: int
    error_message: Optional[str] = None
    explicit_data_type: int  # enum
    explicit_name: Optional[str] = None
    expression: Optional[str | int] = None
    format_string: Optional[int | str] = None
    inferred_data_type: int  # enum
    inferred_name: Optional[str] = None
    is_available_in_mdx: bool
    is_default_image: bool
    is_default_label: bool
    is_hidden: bool
    is_key: bool
    is_nullable: bool
    is_unique: bool
    keep_unique_rows: bool
    lineage_tag: Optional[UUID] = None
    sort_by_column_id: Optional[int] = None
    source_column: Optional[str] = None
    state: int
    summarize_by: int
    system_flags: int
    table_id: int
    table_detail_position: int
    type: int

    modified_time: datetime.datetime
    refreshed_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            children_nodes: list[Column | Measure | AttributeHierarchy] = (
                [self.attribute_hierarchy()] + self.child_measures() + self.sorting_columns() + self.child_columns()
            )
            children_lineage = [p.get_lineage(lineage_type) for p in children_nodes if p is not None]
            return LineageNode(self, lineage_type, children_lineage)
        else:
            parent_nodes: list[Optional[SsasTable]] = [self.table(), self.sort_by_column()] + self.parent_columns()
            parent_lineage = [p.get_lineage(lineage_type) for p in parent_nodes if p is not None]
            return LineageNode(self, lineage_type, parent_lineage)

    def data(self, head: int = 100) -> list[int | float | str]:
        table_name = self.table().name
        ret = self.tabular_model.server.query_dax(
            f"EVALUATE TOPN({head}, SELECTCOLUMNS(ALL('{table_name}'), {self.full_name()}))",
            db_name=self.tabular_model.db_name,
        )
        return [next(iter(row.values())) for row in ret]

    def full_name(self) -> str:
        """Returns the fully qualified name for DAX queries"""
        table_name = self.table().name
        return f"'{table_name}'[{self.explicit_name}]"

    def repr_name(self) -> str:
        if self.explicit_name is not None:
            return self.explicit_name
        if self.inferred_name is not None:
            return self.inferred_name
        return str(self.id)

    def table(self) -> "Table":
        """Returns the table class the column is a part of"""
        return self.tabular_model.tables.find({"id": self.table_id})

    def attribute_hierarchy(self) -> "AttributeHierarchy":
        return self.tabular_model.attribute_hierarchies.find({"id": self.attribute_hierarchy_id})

    def levels(self) -> list["Level"]:
        return self.tabular_model.levels.find_all({"column_id": self.id})

    def child_measures(self) -> list["Measure"]:
        if self.expression is None:
            object_type = "COLUMN"
        else:
            object_type = "CALC_COLUMN"
        dependent_measures = self.tabular_model.calc_dependencies.find_all({
            "referenced_object_type": object_type,
            "referenced_table": self.table().name,
            "referenced_object": self.explicit_name,
        })
        dependent_measure_keys = [(m.table, m.object) for m in dependent_measures]
        return [m for m in self.tabular_model.measures if (m.table().name, m.name) in dependent_measure_keys]

    def parent_measures(self) -> list["Measure"]:
        """Calculated columns can use Measures too :("""
        return []

    def child_columns(self) -> list["Column"]:
        """Only occurs when the column is calculated (expression is not None)"""
        return []

    def parent_columns(self) -> list["Column"]:
        return []

    def sort_by_column(self) -> Optional["Column"]:
        if self.sort_by_column_id is None:
            return None
        return self.tabular_model.columns.find({"id": self.sort_by_column_id})

    def sorting_columns(self) -> list["Column"]:
        """
        This provides the inverse information of sort_by_column
        """
        return self.tabular_model.columns.find_all({"sort_by_column_id": self.id})

    def from_relationships(self) -> list["Relationship"]:
        return self.tabular_model.relationships.find_all({"from_column_id": self.id})

    def to_relationships(self) -> list["Relationship"]:
        return self.tabular_model.relationships.find_all({"to_column_id": self.id})

    def relationships(self) -> list["Relationship"]:
        return self.from_relationships() + self.to_relationships()
