from dataclasses import dataclass, field
from enum import IntEnum
from typing import Annotated, Any, cast

from pydantic import Discriminator, Tag

from ._base_node import LayoutNode
from .sources import AggregationSource, DataSource, LiteralSource, Source, SourceRef


class ExpressionVersion(IntEnum):
    VERSION_1 = 1
    VERSION_2 = 2


class _AnyValueHelper(LayoutNode):
    DefaultValueOverridesAncestors: bool


class AnyValue(LayoutNode):
    AnyValue: _AnyValueHelper


class QueryConditionType(IntEnum):
    """Names defined by myself, but based on query outputs from the query tester."""

    STANDARD = 0
    TOP_N = 2
    MEASURE = 3


class ComparisonKind(IntEnum):
    IS_EQUAL = 0
    IS_GREATER_THAN = 1
    IS_GREATER_THAN_OR_EQUAL_TO = 2
    IS_LESS_THAN = 3
    IS_LESS_THAN_OR_EQUAL_TO = 4

    def get_operator(self) -> str:
        OPERATOR_MAPPING = {  # noqa: N806
            ComparisonKind.IS_EQUAL: "=",
            ComparisonKind.IS_GREATER_THAN: ">",
            ComparisonKind.IS_GREATER_THAN_OR_EQUAL_TO: ">=",
            ComparisonKind.IS_LESS_THAN: "<",
            ComparisonKind.IS_LESS_THAN_OR_EQUAL_TO: "<=",
        }
        if self not in OPERATOR_MAPPING:
            msg = f"No operator is defined for: {self}"
            raise ValueError(msg)
        return OPERATOR_MAPPING[self]


class ComparisonHelper(LayoutNode):
    Left: DataSource
    Right: LiteralSource


@dataclass
class Expression:
    template: str
    source: str
    data: dict[str, str] = field(default_factory=dict)
    expr_type: str = ""

    def to_text(self) -> str:
        if self.data:
            return self.template.format(**self.data)
        return self.template


class ContainsCondition(LayoutNode):
    Contains: ComparisonHelper


class InExpressionHelper(LayoutNode):
    Expressions: list[DataSource]
    Values: list[list[LiteralSource]]

    def vals(self) -> list[str]:
        return [str(y.value()) for x in self.Values for y in x]

    def __repr__(self) -> str:
        source = self.Expressions[0].__repr__()
        return f"In({source}, {', '.join(self.vals())})"


class InTopNExpressionHelper(LayoutNode):
    """Internal representation of the Top N option."""

    Expressions: list[DataSource]
    Table: SourceRef


class InCondition(LayoutNode):
    """In is how "is" and "is not" are internally represented."""

    In: InExpressionHelper | InTopNExpressionHelper

    def __repr__(self) -> str:
        return self.In.__repr__()


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


BasicConditions = ContainsCondition | InCondition | ComparisonCondition


class NotConditionHelper(LayoutNode):
    Expression: BasicConditions


class NotCondition(LayoutNode):
    Not: NotConditionHelper

    def __repr__(self) -> str:
        return f"Not({self.Not.Expression.__repr__()})"


NonCompositeConditions = BasicConditions | NotCondition


class CompositeConditionHelper(LayoutNode):
    Left: NonCompositeConditions
    Right: NonCompositeConditions


class AndCondition(LayoutNode):
    And: CompositeConditionHelper


class OrCondition(LayoutNode):
    Or: CompositeConditionHelper


def get_type(v: Any) -> str:  # noqa: PLR0911
    if isinstance(v, dict):
        if "And" in v:
            return "AndCondition"
        if "Or" in v:
            return "OrCondition"
        if "Left" in v:
            return "NonCompositeConditions"
        if "In" in v:
            return "InCondition"
        if "Not" in v:
            return "NotCondition"
        if "Contains" in v:
            return "ContainsCondition"
        if "Comparison" in v:
            return "ComparisonCondition"
        raise ValueError
    return cast("str", v.__class__.__name__)


ConditionType = Annotated[
    Annotated[NonCompositeConditions, Tag("NonCompositeConditions")]
    | Annotated[AndCondition, Tag("AndCondition")]
    | Annotated[OrCondition, Tag("OrCondition")]
    | Annotated[InCondition, Tag("InCondition")]
    | Annotated[NotCondition, Tag("NotCondition")]
    | Annotated[ContainsCondition, Tag("ContainsCondition")]
    | Annotated[ComparisonCondition, Tag("ComparisonCondition")],
    Discriminator(get_type),
]


class Condition(LayoutNode):
    Condition: ConditionType
    Target: list[Source] | None = None

    def __repr__(self) -> str:
        return f"Condition({self.Condition.__repr__()})"
