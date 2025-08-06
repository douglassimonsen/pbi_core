# ruff: noqa: N815
from enum import IntEnum
from typing import TYPE_CHECKING, Annotated, Any, cast

import pbi_translation
from pydantic import BaseModel, Discriminator, Tag

from ._base_node import LayoutNode
from .condition import Condition
from .sources import AggregationSource, ColumnSource, Entity, MeasureSource, Source
from .visuals.properties.filter_properties import FilterObjects

if TYPE_CHECKING:
    from pbi_core.ssas.server import LocalTabularModel

    from .bookmark import BookmarkFilters
    from .layout import Layout
    from .section import Section


class Direction(IntEnum):
    ASCENDING = 1
    DESCENDING = 2


class Orderby(LayoutNode):
    _parent: "TopNFilterMeta"

    Direction: Direction
    Expression: Source


class PrototypeQueryResult(BaseModel):
    data: list[dict[str, Any]]
    dax_query: str
    column_mapping: dict[str, str]


class PrototypeQuery(LayoutNode):
    Version: int
    From: list["From"]
    Select: list[Source]
    Where: list[Condition] | None = None
    OrderBy: list[Orderby] | None = None

    def table_mapping(self) -> dict[str, str]:
        ret: dict[str, str] = {}
        for table in self.From:
            if table.Name is not None:
                ret[table.Name] = table.Entity
        return ret

    @classmethod
    def unwrap_source(cls, source: Source) -> ColumnSource | MeasureSource:
        if isinstance(source, (ColumnSource, MeasureSource)):
            return source
        if isinstance(source, AggregationSource):
            return cls.unwrap_source(source.Aggregation.Expression)
        breakpoint()
        raise ValueError

    def dependencies(self) -> set[ColumnSource | MeasureSource]:
        ret: set[ColumnSource | MeasureSource] = set()
        ret.update(self.unwrap_source(select) for select in self.Select)
        for where in self.Where or []:
            print(where)
            breakpoint()
        ret.update(self.unwrap_source(order_by.Expression) for order_by in self.OrderBy or [])
        return ret

    def get_data(self, model: "LocalTabularModel") -> PrototypeQueryResult:
        raw_query = self.model_dump_json()
        dax_query = pbi_translation.prototype_query(
            raw_query,
            model.db_name,
            model.server.port,
        )
        data = model.server.query_dax(dax_query.DaxExpression)
        column_mapping = dict(
            zip(
                dax_query.SelectNameToDaxColumnName.Keys,
                dax_query.SelectNameToDaxColumnName.Values,
                strict=False,
            ),
        )
        return PrototypeQueryResult(
            data=data,
            dax_query=dax_query.DaxExpression,
            column_mapping=column_mapping,
        )


class TopNFilterMeta(PrototypeQuery):
    _parent: "_SubqueryHelper2"
    Top: int


class _SubqueryHelper2(LayoutNode):
    _parent: "_SubqueryHelper"

    Query: TopNFilterMeta


class _SubqueryHelper(LayoutNode):
    _parent: "Subquery"

    Subquery: _SubqueryHelper2


class SubQueryType(IntEnum):
    NA = 2


class Subquery(LayoutNode):
    _parent: "VisualFilterExpression"

    Name: str
    Expression: _SubqueryHelper
    Type: SubQueryType


def get_from(v: Any) -> str:
    if isinstance(v, dict):
        if "Entity" in v:
            return "Entity"
        if "Expression" in v:
            return "Subquery"
        msg = f"Unknown Filter: {v.keys()}"
        raise ValueError(msg)
    return cast("str", v.__class__.__name__)


From = Annotated[
    Annotated[Entity, Tag("Entity")] | Annotated[Subquery, Tag("Subquery")],
    Discriminator(get_from),
]


class FilterExpression(LayoutNode):
    _parent: "Filter"

    Version: int
    From: list["From"]
    Where: list[Condition]


class HowCreated(IntEnum):
    AUTOMATIC = 0
    MANUAL = 1
    NA = 4
    NA2 = 5


class Filter(LayoutNode):
    name: str | None = None
    type: str
    howCreated: HowCreated
    expression: Source
    isLockedInViewMode: bool = False
    isHiddenInViewMode: bool = False
    objects: FilterObjects | None = None
    filter: FilterExpression | None = None
    displayName: str | None = None
    ordinal: int = 0
    cachedDisplayNames: Any = None
    isLinkedAsAggregation: bool = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.displayName or self.name})"

    def __str__(self) -> str:
        return super().__str__()


class VisualFilterExpression(LayoutNode):
    _parent: "VisualFilter"

    Version: int | None = None
    From: list["From"] | None = None
    Where: list[Condition]


# Filter specialization, only done to create better type completion.
# Visual needs extra fields because it allows measure sources I think


class VisualFilter(Filter):
    restatement: str | None = None
    filterExpressionMetadata: Any | None = None

    def to_bookmark(self) -> "BookmarkFilter":
        return cast("BookmarkFilter", self)


class BookmarkFilter(VisualFilter):
    _parent: "BookmarkFilters"


class PageFilter(Filter):
    _parent: "Section"


class GlobalFilter(Filter):
    _parent: "Layout"
