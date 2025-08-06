from enum import IntEnum
from typing import TYPE_CHECKING, Any, Optional, cast

from ._base_node import LayoutNode
from .condition import Condition
from .sources import AggregationSource, ColumnSource, Entity, MeasureSource, Source

if TYPE_CHECKING:
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


class PrototypeQuery(LayoutNode):
    Version: int
    From: list[Entity]
    Select: list[Source]
    Where: Optional[list[Condition]] = None
    OrderBy: Optional[list[Orderby]] = None

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
        elif isinstance(source, AggregationSource):
            return cls.unwrap_source(source.Aggregation.Expression)
        else:
            breakpoint()
            raise ValueError

    def dependencies(self) -> set[ColumnSource | MeasureSource]:
        ret: set[ColumnSource | MeasureSource] = set()
        for select in self.Select:
            ret.add(self.unwrap_source(select))
        for where in self.Where or []:
            print(where)
            breakpoint()
        for order_by in self.OrderBy or []:
            ret.add(self.unwrap_source(order_by.Expression))
        return ret


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


class FilterExpression(LayoutNode):
    _parent: "Filter"

    Version: int
    From: list[Entity]
    Where: list[Condition]


class HowCreated(IntEnum):
    AUTOMATIC = 0
    MANUAL = 1
    NA = 4
    NA2 = 5


class Filter(LayoutNode):
    name: Optional[str] = None
    type: str
    howCreated: HowCreated
    expression: Source
    isLockedInViewMode: bool = False
    isHiddenInViewMode: bool = False
    objects: Any = None
    filter: Optional[FilterExpression] = None
    displayName: Optional[str] = None
    ordinal: int = 0
    cachedDisplayNames: Any = None
    isLinkedAsAggregation: bool = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.displayName or self.name})"


class VisualFilterExpression(LayoutNode):
    _parent: "VisualFilter"

    Version: Optional[int] = None
    From: Optional[list[Entity | Subquery]] = None
    Where: list[Condition]


# Filter specialization, only done to create better type completion.
# Visual needs extra fields because it allows measure sources I think


class VisualFilter(Filter):
    restatement: Optional[str] = None
    filterExpressionMetadata: Optional[Any] = None

    def to_bookmark(self) -> "BookmarkFilter":
        return cast(BookmarkFilter, self)


class BookmarkFilter(VisualFilter):
    _parent: "BookmarkFilters"


class PageFilter(Filter):
    _parent: "Section"


class GlobalFilter(Filter):
    _parent: "Layout"
