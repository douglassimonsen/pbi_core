from typing import TYPE_CHECKING

from attrs import field
from structlog import BoundLogger

from pbi_core.attrs import define
from pbi_core.logging import get_logger
from pbi_core.ssas.model_tables.base import SsasRenameRecord
from pbi_core.ssas.server._commands import RenameCommands
from pbi_core.ssas.server.utils import SsasCommands
from pbi_core.static_files.layout.filters import Filter
from pbi_core.static_files.layout.sources.base import Entity, Source, SourceRef
from pbi_core.static_files.layout.sources.column import ColumnSource
from pbi_core.static_files.layout.sources.hierarchy import HierarchySource, _PropertyVariationSourceHelper
from pbi_core.static_files.layout.visuals.base import BaseVisual

from . import set_name
from .commands import CommandMixin

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables.base.base_ssas_table import SsasTable
    from pbi_core.static_files.layout._base_node import LayoutNode
    from pbi_core.static_files.layout.layout import Layout


logger: BoundLogger = get_logger()


@define()
class Column(CommandMixin, SsasRenameRecord):  # pyright: ignore[reportIncompatibleMethodOverride]
    """A column of an SSAS table.

    PowerBI spec: [Power BI](https://learn.microsoft.com/en-us/analysis-services/tabular-models/column-properties-ssas-tabular?view=asallproducts-allversions)

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/00a9ec7a-5f4d-4517-8091-b370fe2dc18b)
    """

    _commands: RenameCommands = field(default=SsasCommands.column, init=False, repr=False)

    def __repr__(self) -> str:
        return f"Column({self.id}: {self.full_name()})"

    def parents(self, *, recursive: bool = False) -> "frozenset[SsasTable]":
        """Returns all columns and measures this Column is dependent on."""
        base_deps = {self.table()} | self.parent_columns() | self.parent_measures()
        if sort_by_column := self.sort_by_column():
            base_deps.add(sort_by_column)
        frozen_base_deps = frozenset(base_deps)

        if recursive:
            return self._recurse_parents(frozen_base_deps)
        return frozen_base_deps

    def children(self, *, recursive: bool = False) -> "frozenset[SsasTable]":
        """Returns all columns and measures dependent on this Column."""
        full_dependencies = frozenset(
            {self.attribute_hierarchy()}
            | self.child_columns()
            | self.child_measures()
            | self.sorting_columns()
            | self.child_variations()
            | self.child_default_variations(),
        )
        if recursive:
            return self._recurse_children(full_dependencies)
        return full_dependencies

    def set_name(self, new_name: str, layout: "Layout") -> None:
        """Renames the column and update any dependent expressions to use the new name.

        Since measures are referenced by name in DAX expressions, renaming a measure will break any dependent
        expressions.
        """
        columns = _get_columns_sources(self, layout)
        for c in columns:
            c.Column.Property = new_name
            if c.NativeReferenceName == self.name():
                c.NativeReferenceName = new_name
        hierarchies = _get_hierarchies_sources(self, layout)
        for h in hierarchies:
            if isinstance(h.Hierarchy.Expression, SourceRef):
                h.Hierarchy.Hierarchy = new_name
            elif isinstance(h.Hierarchy.Expression, _PropertyVariationSourceHelper):
                h.Hierarchy.Expression.PropertyVariationSource.Property = new_name
            else:
                h.Hierarchy.Hierarchy = new_name
        set_name.fix_dax(self, new_name)
        self.explicit_name = new_name


def _get_matching_columns(n: "LayoutNode", entity_mapping: dict[str, str], column: "Column") -> list[ColumnSource]:
    columns = []
    for c in n.find_all(ColumnSource):
        if c.Column.Property != column.name():
            continue

        if isinstance(c.Column.Expression, SourceRef):
            src = c.Column.Expression.SourceRef
        else:
            src = c.Column.Expression.TransformTableRef

        if isinstance(src, Source):
            if entity_mapping[src.Source] == column.table().name:
                columns.append(c)
        elif src.Entity == column.table().name:
            columns.append(c)

    return columns


def _get_columns_sources(column: "Column", layout: "Layout") -> list[ColumnSource]:
    columns = []
    visuals = layout.find_all(BaseVisual)
    for v in visuals:
        if v.prototypeQuery is None:
            continue
        entity_mapping = {
            e.Name: e.Entity for e in v.prototypeQuery.From if isinstance(e, Entity) and e.Name is not None
        }
        columns.extend(_get_matching_columns(v, entity_mapping, column))

    filters = layout.find_all(Filter)
    for f in filters:
        entity_mapping = {}
        if f.filter is not None:
            entity_mapping = {e.Name: e.Entity for e in f.filter.From if isinstance(e, Entity) and e.Name is not None}
        columns.extend(_get_matching_columns(f, entity_mapping, column))
    return columns


def _get_matching_hierarchies(
    n: "LayoutNode",
    entity_mapping: dict[str, str],
    column: "Column",
) -> list[HierarchySource]:
    hierarchies = []

    for h in n.find_all(HierarchySource):
        if isinstance(h.Hierarchy.Expression, SourceRef):
            table_name = h.Hierarchy.Expression.table(entity_mapping)
            column_name = h.Hierarchy.Hierarchy
        if isinstance(h.Hierarchy.Expression, _PropertyVariationSourceHelper):
            table_name = h.Hierarchy.Expression.PropertyVariationSource.Expression.table(entity_mapping)
            column_name = h.Hierarchy.Expression.PropertyVariationSource.Property
        else:
            table_name = h.Hierarchy.Expression.table(entity_mapping)
            column_name = h.Hierarchy.Hierarchy

        if column_name == column.name() and table_name == column.table().name:
            hierarchies.append(h)
    return hierarchies


def _get_hierarchies_sources(column: "Column", layout: "Layout") -> list[HierarchySource]:
    hierarchies = []
    visuals = layout.find_all(BaseVisual)
    for v in visuals:
        if v.prototypeQuery is None:
            continue
        entity_mapping = {
            e.Name: e.Entity for e in v.prototypeQuery.From if isinstance(e, Entity) and e.Name is not None
        }
        hierarchies.extend(_get_matching_hierarchies(v, entity_mapping, column))

    return hierarchies
