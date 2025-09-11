import datetime
from typing import TYPE_CHECKING, ClassVar
from uuid import UUID, uuid4

from pydantic import PrivateAttr
from structlog import BoundLogger

from pbi_core.logging import get_logger
from pbi_core.ssas.model_tables.base import SsasRenameRecord
from pbi_core.ssas.model_tables.enums import DataState, DataType
from pbi_core.ssas.server._commands import RenameCommands
from pbi_core.ssas.server.utils import SsasCommands
from pbi_core.static_files.layout.filters import Filter
from pbi_core.static_files.layout.sources.base import Entity, SourceRef
from pbi_core.static_files.layout.sources.column import ColumnSource
from pbi_core.static_files.layout.visuals.base import BaseVisual

from ....static_files.layout.sources.base import Source
from . import set_name
from .commands import CommandMixin
from .enums import Alignment, ColumnType, EncodingHint, SummarizedBy

if TYPE_CHECKING:
    from pbi_core.static_files.layout._base_node import LayoutNode
    from pbi_core.static_files.layout.layout import Layout


logger: BoundLogger = get_logger()


class Column(SsasRenameRecord, CommandMixin):  # pyright: ignore[reportIncompatibleMethodOverride]
    """A column of an SSAS table.

    PowerBI spec: [Power BI](https://learn.microsoft.com/en-us/analysis-services/tabular-models/column-properties-ssas-tabular?view=asallproducts-allversions)

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/00a9ec7a-5f4d-4517-8091-b370fe2dc18b)
    """

    _field_mapping: ClassVar[dict[str, str]] = {
        "description": "Description",
    }
    _db_name_field: str = "ExplicitName"
    _repr_name_field: str = "explicit_name"
    _read_only_fields = ("table_id",)

    alignment: Alignment
    attribute_hierarchy_id: int
    column_origin_id: int | None = None
    column_storage_id: int
    data_category: str | None = None
    description: str | None = None
    display_folder: str | None = None
    display_ordinal: int
    encoding_hint: EncodingHint
    error_message: str | None = None
    explicit_data_type: DataType  # enum
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
    state: DataState
    summarize_by: SummarizedBy
    system_flags: int
    table_id: int
    table_detail_position: int
    type: ColumnType

    modified_time: datetime.datetime
    refreshed_time: datetime.datetime
    structure_modified_time: datetime.datetime

    _commands: RenameCommands = PrivateAttr(default_factory=lambda: SsasCommands.column)

    def __repr__(self) -> str:
        return f"Column({self.table().name}.{self.pbi_core_name()})"

    def set_name(self, new_name: str, layout: "Layout") -> None:
        def get_matching_columns(c: ColumnSource) -> bool:
            if c.Column.Property != self.explicit_name:
                return False
            if not isinstance(c.Column.Expression, SourceRef):
                return False
            return c.Column.Expression.SourceRef.table() == self.table().name

        """Renames the column and update any dependent expressions to use the new name.

        Since measures are referenced by name in DAX expressions, renaming a measure will break any dependent
        expressions.
        """
        columns = _get_columns_sources(self, layout)
        for c in columns:
            c.Column.Property = new_name
            if c.NativeReferenceName == self.explicit_name:
                c.NativeReferenceName = new_name
        set_name.fix_dax(self, new_name)
        self.explicit_name = new_name

    def modification_hash(self) -> int:
        return hash((
            self.explicit_name,
            self.description,
            self.display_folder,
            self.format_string,
            self.is_hidden,
            self.summarize_by,
            self.expression,
        ))


def _get_matching_columns(n: "LayoutNode", entity_mapping: dict[str, str], column: "Column") -> list[ColumnSource]:
    columns = []
    for c in n.find_all(ColumnSource):
        if c.Column.Property != column.explicit_name:
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
