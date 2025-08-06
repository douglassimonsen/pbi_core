import inspect
from enum import IntEnum
from typing import Annotated, Any, Optional, Union

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


class ComparisonKind(IntEnum):
    IS_BLANK = 0
    IS_GREATER_THAN = 1
    IS_GREATER_THAN_OR_EQUAL_TO = 2
    IS_LESS_THAN = 3
    IS_LESS_THAN_OR_EQUAL_TO = 4


class ComparisonHelper(LayoutNode):
    Left: DataSource
    Right: LiteralSource


class ContainsCondition(LayoutNode):
    Contains: ComparisonHelper


class InExpressionHelper(LayoutNode):
    Expressions: list[DataSource]
    Values: list[list[LiteralSource]]

    def __repr__(self) -> str:
        vals = [str(y.value) for x in self.Values for y in x]
        source = self.Expressions[0].__repr__()
        return f"In({source}, {', '.join(vals)})"


class InTopNExpressionHelper(LayoutNode):
    Expressions: list[DataSource]
    Table: SourceRef


class InCondition(LayoutNode):
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
        return v.__class__.__name__


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
