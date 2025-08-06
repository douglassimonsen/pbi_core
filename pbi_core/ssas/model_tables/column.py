import datetime
from typing import TYPE_CHECKING, ClassVar, Optional
from uuid import UUID

from ..server.tabular_model import SsasTable

if TYPE_CHECKING:
    from .attribute_hierarchy import AttributeHierarchy
    from .level import Level
    from .relationship import Relationship
    from .table import Table


class Column(SsasTable):
    _field_mapping: ClassVar[dict[str, str]] = {
        "description": "Description",
    }
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

    def data(self, head: int = 100) -> list[dict[str, str]]:
        table_name = self.table().name
        ret = self.tabular_model.server.query_dax(
            f"EVALUATE TOPN({head}, SELECTCOLUMNS(ALL('{table_name}'), '{table_name}'[{self.explicit_name}]))",
            db_name=self.tabular_model.db_name,
        )
        return [next(iter(row.values())) for row in ret]

    def repr_name(self) -> str:
        if self.explicit_name is not None:
            return self.explicit_name
        if self.inferred_name is not None:
            return self.inferred_name
        return str(self.id)

    def table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.table_id})

    def attribute_hierarchy(self) -> Optional["AttributeHierarchy"]:
        return self.tabular_model.attribute_hierarchies.find({"id": self.attribute_hierarchy_id})

    def levels(self) -> list["Level"]:
        return self.tabular_model.levels.find_all({"column_id": self.id})

    def sort_by_column(self) -> "Column":
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
