import inspect
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Optional, cast

from ._base_node import LayoutNode
from .condition import Condition
from .sources import Entity, Source
from .sources.aggregation import AggregationSource
from .sources.column import ColumnSource

if TYPE_CHECKING:
    from .bookmark import BookmarkFilters
    from .layout import Layout
    from .section import Section


class Direction(IntEnum):
    ASCENDING = 1
    DESCENDING = 2


class Orderby(LayoutNode):
    parent: "TopNFilterMeta"

    Direction: Direction
    Expression: Source


class PrototypeQuery(LayoutNode):
    Version: int
    From: list[Entity]
    Select: list[Source]
    Where: Optional[list[Condition]] = None
    OrderBy: Optional[list[Orderby]] = None

    def dependencies(self) -> set[ColumnSource]:
        ret = set()
        for select in self.Select:
            if isinstance(select, ColumnSource):
                ret.add(select)
            elif isinstance(select, AggregationSource):
                if isinstance(select.Aggregation.Expression, ColumnSource):
                    ret.add(select.Aggregation.Expression)
        for where in self.Where or []:
            breakpoint()
        for order_by in self.OrderBy or []:
            if isinstance(order_by.Expression, ColumnSource):
                ret.add(order_by.Expression)
            elif isinstance(order_by.Expression, AggregationSource):
                if isinstance(order_by.Expression.Aggregation.Expression, ColumnSource):
                    ret.add(order_by.Expression.Aggregation.Expression)
        return ret


class TopNFilterMeta(PrototypeQuery):
    parent: "_SubqueryHelper2"
    Top: int


class _SubqueryHelper2(LayoutNode):
    parent: "_SubqueryHelper"

    Query: TopNFilterMeta


class _SubqueryHelper(LayoutNode):
    parent: "Subquery"

    Subquery: _SubqueryHelper2


class SubQueryType(IntEnum):
    NA = 2


class Subquery(LayoutNode):
    parent: "VisualFilterExpression"

    Name: str
    Expression: _SubqueryHelper
    Type: SubQueryType


class FilterExpression(LayoutNode):
    parent: "Filter"

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
        if self.displayName is not None:
            return str(super().__repr__())
        else:
            return f"{self.__class__.__name__}({self.name})"


class VisualFilterExpression(LayoutNode):
    parent: "VisualFilter"

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
    parent: "BookmarkFilters"


class PageFilter(Filter):
    parent: "Section"


class GlobalFilter(Filter):
    parent: "Layout"


"""
woo boy. Why is this code here? Well, we want a parent attribute on the objects to make user navigation easier
This has to be a non-private attribute due to a bug in pydantic right now.
We know we'll add the parent attribute after pydantic does it's work, but we want mypy to think the parent is
always there. Therefore we check all objects with parents and make the default None so the "is_required" becomes False
https://github.com/pydantic/pydantic/blob/a764871df98c8932e9b7bc10d861053d110a99e4/pydantic/fields.py#L572
"""
for name, obj in list(globals().items()):
    if inspect.isclass(obj) and issubclass(obj, LayoutNode) and "parent" in obj.model_fields:
        obj.model_fields["parent"].default = None
