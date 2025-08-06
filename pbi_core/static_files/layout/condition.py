from enum import IntEnum
from typing import TYPE_CHECKING, Annotated, Any, Optional, Union, cast

from pydantic import Discriminator, Tag

from ._base_node import LayoutNode
from .sources import AggregationSource, DataSource, LiteralSource, Source, SourceRef

if TYPE_CHECKING:
    from .filters import From


class ExpressionVersion(IntEnum):
    VERSION_1 = 1
    VERSION_2 = 2


class _AnyValueHelper(LayoutNode):
    DefaultValueOverridesAncestors: bool


class AnyValue(LayoutNode):
    AnyValue: _AnyValueHelper


class QueryConditionType(IntEnum):
    """Names defined by myself, but based on query outputs from the query tester"""

    STANDARD = 0
    SLOW = 1  # Currently, just the search options
    TOP_N = 2
    MEASURE = 3


class ComparisonKind(IntEnum):
    IS_BLANK = 0
    IS_GREATER_THAN = 1
    IS_GREATER_THAN_OR_EQUAL_TO = 2
    IS_LESS_THAN = 3
    IS_LESS_THAN_OR_EQUAL_TO = 4

    def get_operator(self) -> str:
        OPERATOR_MAPPING = {
            ComparisonKind.IS_GREATER_THAN: ">",
            ComparisonKind.IS_GREATER_THAN_OR_EQUAL_TO: ">=",
            ComparisonKind.IS_LESS_THAN: "<",
            ComparisonKind.IS_LESS_THAN_OR_EQUAL_TO: "<=",
        }
        if self not in OPERATOR_MAPPING:
            raise ValueError(f"No operator is defined for: {self}")
        return OPERATOR_MAPPING[self]


class ComparisonHelper(LayoutNode):
    Left: DataSource
    Right: LiteralSource


class ContainsCondition(LayoutNode):
    Contains: ComparisonHelper

    def get_prototype_query_type(self) -> QueryConditionType:
        return QueryConditionType.SLOW

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        breakpoint()


class InExpressionHelper(LayoutNode):
    Expressions: list[DataSource]
    Values: list[list[LiteralSource]]

    def vals(self) -> list[str]:
        return [str(y.value()) for x in self.Values for y in x]

    def __repr__(self) -> str:
        source = self.Expressions[0].__repr__()
        return f"In({source}, {', '.join(self.vals())})"

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        table_name: str = tables[self.Expressions[0].Column.table()].Entity  # type: ignore
        column_name: str = self.Expressions[0].Column.column()  # type: ignore
        vals = ", ".join(self.vals())
        return f"'{table_name}'[{column_name}] IN {{{vals}}}"


class InTopNExpressionHelper(LayoutNode):
    """Internal representation of the Top N option"""

    Expressions: list[DataSource]
    Table: SourceRef

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        breakpoint()


class InCondition(LayoutNode):
    """In is how "is" and "is not" are internally represented"""

    In: InExpressionHelper | InTopNExpressionHelper

    def __repr__(self) -> str:
        return self.In.__repr__()

    def get_prototype_query_type(self) -> QueryConditionType:
        if isinstance(self.In, InTopNExpressionHelper):
            return QueryConditionType.TOP_N
        return QueryConditionType.STANDARD

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        return self.In.to_query_text(tables)


class TimeUnit(IntEnum):
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4
    WEEK = 5
    MONTH = 6
    QUARTER = 7
    YEAR = 8


class _NowHelper(LayoutNode):
    Now: dict[str, str]  # actually an empty string


class _DateSpanHelper(LayoutNode):
    Expression: LiteralSource | _NowHelper
    TimeUnit: TimeUnit


class DateSpan(LayoutNode):
    DateSpan: _DateSpanHelper


class ComparisonConditionHelper(LayoutNode):
    ComparisonKind: ComparisonKind
    Left: DataSource | AggregationSource
    Right: LiteralSource | AnyValue | DateSpan


class ComparisonCondition(LayoutNode):
    Comparison: ComparisonConditionHelper

    def get_prototype_query_type(self) -> QueryConditionType:
        if isinstance(self.Comparison.Left, AggregationSource):
            return QueryConditionType.MEASURE
        return QueryConditionType.STANDARD

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        if isinstance(self.Comparison.Left, AggregationSource):
            raise ValueError
        else:
            table_name: str = tables[self.Comparison.Left.Column.table()].Entity  # type: ignore
            column_name: str = self.Comparison.Left.Column.column()  # type: ignore
            if self.Comparison.ComparisonKind == ComparisonKind.IS_BLANK:
                return f"ISBLANK('{table_name}'[{column_name}])"
            assert isinstance(self.Comparison.Right, LiteralSource)
            value = self.Comparison.Right.value()
            return f"'{table_name}'[{column_name}] {self.Comparison.ComparisonKind.get_operator()} {value}"


BasicConditions = ContainsCondition | InCondition | ComparisonCondition


class NotConditionHelper(LayoutNode):
    Expression: BasicConditions


class NotCondition(LayoutNode):
    Not: NotConditionHelper

    def __repr__(self) -> str:
        return f"Not({self.Not.Expression.__repr__()})"

    def get_prototype_query_type(self) -> QueryConditionType:
        return self.Not.Expression.get_prototype_query_type()

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        return f"NOT({self.Not.Expression.to_query_text(tables)})"


NonCompositeConditions = BasicConditions | NotCondition


class CompositeConditionHelper(LayoutNode):
    Left: NonCompositeConditions
    Right: NonCompositeConditions

    def get_prototype_query_type(self) -> QueryConditionType:
        types = tuple(sorted({self.Left.get_prototype_query_type(), self.Right.get_prototype_query_type()}))
        if len(types) == 1:
            return types[0]
        if types == (QueryConditionType.STANDARD, QueryConditionType.SLOW):
            return QueryConditionType.SLOW
        raise ValueError(types)

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        return f"{self.Left.to_query_text(tables)}, {self.Right.to_query_text(tables)}"


class AndCondition(LayoutNode):
    And: CompositeConditionHelper

    def get_prototype_query_type(self) -> QueryConditionType:
        return self.And.get_prototype_query_type()

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        return f"AND({self.And.to_query_text(tables)})"


class OrCondition(LayoutNode):
    Or: CompositeConditionHelper

    def get_prototype_query_type(self) -> QueryConditionType:
        return self.Or.get_prototype_query_type()

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        return f"OR({self.Or.to_query_text(tables)})"


def get_type(v: Any) -> str:
    if isinstance(v, dict):
        if "And" in v.keys():
            return "AndCondition"
        elif "Or" in v.keys():
            return "OrCondition"
        elif "Left" in v.keys():
            return "NonCompositeConditions"
        elif "In" in v.keys():
            return "InCondition"
        elif "Not" in v.keys():
            return "NotCondition"
        elif "Contains" in v.keys():
            return "ContainsCondition"
        elif "Comparison" in v.keys():
            return "ComparisonCondition"
        raise ValueError
    else:
        return cast(str, v.__class__.__name__)


ConditionType = Annotated[
    Union[
        Annotated[NonCompositeConditions, Tag("NonCompositeConditions")],
        Annotated[AndCondition, Tag("AndCondition")],
        Annotated[OrCondition, Tag("OrCondition")],
        Annotated[InCondition, Tag("InCondition")],
        Annotated[NotCondition, Tag("NotCondition")],
        Annotated[ContainsCondition, Tag("ContainsCondition")],
        Annotated[ComparisonCondition, Tag("ComparisonCondition")],
    ],
    Discriminator(get_type),
]


class Condition(LayoutNode):
    Condition: ConditionType
    Target: Optional[list[Source]] = None

    def __repr__(self) -> str:
        return f"Condition({self.Condition.__repr__()})"

    def get_prototype_query_type(self) -> QueryConditionType:
        return self.Condition.get_prototype_query_type()

    def to_query_text(self, tables: dict[str, "From"]) -> str:
        return self.Condition.to_query_text(tables)
