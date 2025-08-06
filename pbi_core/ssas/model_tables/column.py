import datetime
from typing import TYPE_CHECKING, ClassVar, Literal
from uuid import UUID, uuid4

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasRenameTable, SsasTable

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
    column_origin_id: int | None = None
    column_storage_id: int
    data_category: str | None = None
    description: str | None = None
    display_folder: str | None = None
    display_ordinal: int
    encoding_hint: int
    error_message: str | None = None
    explicit_data_type: int  # enum
    explicit_name: str | None = None
    expression: str | int | None = None
    format_string: int | str | None = None
    inferred_data_type: int  # enum
    inferred_name: str | None = None
    is_available_in_mdx: bool
    is_default_image: bool
    is_default_label: bool
    is_hidden: bool
    is_key: bool
    is_nullable: bool
    is_unique: bool
    keep_unique_rows: bool
    lineage_tag: UUID = uuid4()
    sort_by_column_id: int | None = None
    source_column: str | None = None
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
            children_nodes: list[Column | Measure | AttributeHierarchy] = [
                self.attribute_hierarchy(),
                *self.child_measures(),
                *self.sorting_columns(),
                *self.child_columns(),
            ]
            children_lineage = [p.get_lineage(lineage_type) for p in children_nodes if p is not None]
            return LineageNode(self, lineage_type, children_lineage)
        parent_nodes: list[SsasTable | None] = [
            self.table(),
            self.sort_by_column(),
            *self.parent_columns(),
            *self.parent_measures(),
        ]
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
        """Returns the fully qualified name for DAX queries."""
        table_name = self.table().name
        return f"'{table_name}'[{self.explicit_name}]"

    def pbi_core_name(self) -> str:
        """Returns the name displayed in the PBIX report."""
        if self.explicit_name is not None:
            return self.explicit_name
        if self.inferred_name is not None:
            return self.inferred_name
        return str(self.id)

    def __repr__(self) -> str:
        return f"Column({self.table().name}.{self.pbi_core_name()})"

    def table(self) -> "Table":
        """Returns the table class the column is a part of."""
        return self.tabular_model.tables.find({"id": self.table_id})

    def attribute_hierarchy(self) -> "AttributeHierarchy":
        return self.tabular_model.attribute_hierarchies.find({"id": self.attribute_hierarchy_id})

    def levels(self) -> set["Level"]:
        return self.tabular_model.levels.find_all({"column_id": self.id})

    def _column_type(self) -> Literal["COLUMN", "CALC_COLUMN"]:
        if self.expression is None:
            return "COLUMN"
        return "CALC_COLUMN"

    def child_measures(self, *, recursive: bool = False) -> set["Measure"]:
        """Returns measures dependent on this Column."""
        object_type = self._column_type()
        dependent_measures = self.tabular_model.calc_dependencies.find_all({
            "referenced_object_type": object_type,
            "referenced_table": self.table().name,
            "referenced_object": self.explicit_name,
            "object_type": "MEASURE",
        })
        child_keys: list[tuple[str | None, str]] = [(m.table, m.object) for m in dependent_measures]
        full_dependencies = [m for m in self.tabular_model.measures if (m.table().name, m.name) in child_keys]

        if recursive:
            recursive_dependencies: set[Measure] = set()
            for dep in full_dependencies:
                if f"[{self.explicit_name}]" in str(dep.expression):
                    recursive_dependencies.add(dep)
                    recursive_dependencies.update(dep.child_measures(recursive=True))
            return recursive_dependencies

        return {x for x in full_dependencies if f"[{self.explicit_name}]" in str(x.expression)}

    def parent_measures(self, *, recursive: bool = False) -> set["Measure"]:
        """Returns measures this column is dependent on.

        Note:
        ----
            Calculated columns can use Measures too :(.

        """
        object_type = self._column_type()
        dependent_measures = self.tabular_model.calc_dependencies.find_all({
            "object_type": object_type,
            "table": self.table().name,
            "object": self.explicit_name,
            "referenced_object_type": "MEASURE",
        })
        parent_keys = [(m.referenced_table, m.referenced_object) for m in dependent_measures]
        full_dependencies = [m for m in self.tabular_model.measures if (m.table().name, m.name) in parent_keys]

        if recursive:
            recursive_dependencies: set[Measure] = set()
            for dep in full_dependencies:
                if f"[{dep.name}]" in str(self.expression):
                    recursive_dependencies.add(dep)
                    recursive_dependencies.update(dep.parent_measures(recursive=True))
            return recursive_dependencies

        return {x for x in full_dependencies if f"[{x.name}]" in str(self.expression)}

    def child_columns(self, *, recursive: bool = False) -> set["Column"]:
        """Returns columns dependent on this Column.

        Note:
        ----
            Only occurs when the dependent column is calculated (expression is not None).

        """
        object_type = self._column_type()
        dependent_measures = self.tabular_model.calc_dependencies.find_all({
            "referenced_object_type": object_type,
            "referenced_table": self.table().name,
            "referenced_object": self.explicit_name,
        })
        assert all(m.table is not None for m in dependent_measures)
        child_keys: list[tuple[str, str]] = [  # pyright: ignore reportAssignmentType
            (m.table, m.object) for m in dependent_measures if m.object_type in {"CALC_COLUMN", "COLUMN"}
        ]
        full_dependencies = [m for m in self.tabular_model.columns if (m.table().name, m.explicit_name) in child_keys]

        if recursive:
            recursive_dependencies: set[Column] = set()
            for dep in full_dependencies:
                if f"[{self.explicit_name}]" in str(dep.expression):
                    recursive_dependencies.add(dep)
                    recursive_dependencies.update(dep.child_columns(recursive=True))
            return recursive_dependencies

        return {x for x in full_dependencies if f"[{self.explicit_name}]" in str(x.expression)}

    def parent_columns(self, *, recursive: bool = False) -> set["Column"]:
        """Returns Columns this Column is dependent on.

        Note:
        ----
            Only occurs when column is calculated.

        """
        object_type = self._column_type()
        if object_type == "COLUMN":
            return set()
        dependent_measures = self.tabular_model.calc_dependencies.find_all({
            "object_type": object_type,
            "table": self.table().name,
            "object": self.explicit_name,
        })
        parent_keys = {
            (m.referenced_table, m.referenced_object)
            for m in dependent_measures
            if m.referenced_object_type in {"CALC_COLUMN", "COLUMN"}
        }
        full_dependencies = [c for c in self.tabular_model.columns if (c.table().name, c.explicit_name) in parent_keys]

        if recursive:
            recursive_dependencies: set[Column] = set()
            for dep in full_dependencies:
                if f"[{dep.explicit_name}]" in str(self.expression):
                    recursive_dependencies.add(dep)
                    recursive_dependencies.update(dep.parent_columns(recursive=True))
            return recursive_dependencies

        return {x for x in full_dependencies if f"[{x.explicit_name}]" in str(self.expression)}

    def parents(self, *, recursive: bool = False) -> "set[Column | Measure]":
        """Returns all columns and measures this Column is dependent on."""
        full_dependencies = self.parent_columns() | self.parent_measures()
        if recursive:
            recursive_dependencies: set[Column | Measure] = set()
            for dep in full_dependencies:
                recursive_dependencies.add(dep)
                recursive_dependencies.update(dep.parents(recursive=True))
            return recursive_dependencies

        return full_dependencies

    def children(self, *, recursive: bool = False) -> "set[Column | Measure]":
        """Returns all columns and measures dependent on this Column."""
        full_dependencies = self.child_columns() | self.child_measures()
        if recursive:
            recursive_dependencies: set[Column | Measure] = set()
            for dep in full_dependencies:
                recursive_dependencies.add(dep)
                recursive_dependencies.update(dep.children(recursive=True))
            return recursive_dependencies
        return full_dependencies

    def sort_by_column(self) -> "Column | None":
        if self.sort_by_column_id is None:
            return None
        return self.tabular_model.columns.find({"id": self.sort_by_column_id})

    def sorting_columns(self) -> set["Column"]:
        """Provides the inverse information of sort_by_column."""
        return self.tabular_model.columns.find_all({"sort_by_column_id": self.id})

    def from_relationships(self) -> set["Relationship"]:
        return self.tabular_model.relationships.find_all({"from_column_id": self.id})

    def to_relationships(self) -> set["Relationship"]:
        return self.tabular_model.relationships.find_all({"to_column_id": self.id})

    def relationships(self) -> set["Relationship"]:
        return self.from_relationships() | self.to_relationships()
