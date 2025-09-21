from enum import IntEnum
from typing import Annotated, Any

from attrs import field
from pydantic import Discriminator, Tag

from pbi_core.pydantic.attrs import define
from pbi_core.static_files.layout._base_node import LayoutNode

from .column import ColumnSource
from .hierarchy import HierarchyLevelSource
from .measure import MeasureSource


@define()
class ExpressionName(LayoutNode):
    ExpressionName: str


@define()
class SelectRef(LayoutNode):
    SelectRef: ExpressionName


def get_expression_type(v: object | dict[str, Any]) -> str:
    if isinstance(v, dict):
        if "Aggregation" in v:
            return "AggregationSource"
        if any(c in v for c in ("Column", "Measure", "HierarchyLevel")):
            return "DataSource"
        if "SelectRef" in v:
            return "SelectRef"
        raise TypeError(v)
    return v.__class__.__name__


@define()
class AllRolesRef(LayoutNode):
    AllRolesRef: dict[str, bool] = field(factory=dict)  # no values have been seen in this field


@define()
class ScopedEval2(LayoutNode):
    Expression: "ScopedEvalExpression"
    Scope: list[AllRolesRef]


# TODO: merge with ScopedEvalArith
@define()
class ScopedEvalAgg(LayoutNode):  # copied from arithmetic.py to avoid circular dependencies
    ScopedEval: ScopedEval2


def get_data_source_type(v: object | dict[str, Any]) -> str:
    if isinstance(v, dict):
        if "Column" in v:
            return "ColumnSource"
        if "Measure" in v:
            return "MeasureSource"
        if "HierarchyLevel" in v:
            return "HierarchyLevelSource"
        if "ScopedEval" in v:  # Consider subclassing? This only happens for color gradient properties IME
            return "ScopedEvalAgg"
        raise TypeError(v)
    return v.__class__.__name__


DataSource = Annotated[
    Annotated[ColumnSource, Tag("ColumnSource")]
    | Annotated[MeasureSource, Tag("MeasureSource")]
    | Annotated[HierarchyLevelSource, Tag("HierarchyLevelSource")]
    | Annotated[ScopedEvalAgg, Tag("ScopedEvalAgg")],
    Discriminator(get_data_source_type),
]


class AggregationFunction(IntEnum):
    SUM = 0
    AVERAGE = 1
    COUNT = 2
    MIN = 3
    MAX = 4
    DISTINCT_COUNT = 5
    MEDIAN = 6
    STD_DEV_P = 7
    VAR_P = 8


@define()
class _AggregationSourceHelper(LayoutNode):
    Expression: DataSource
    Function: AggregationFunction


@define()
class AggregationSource(LayoutNode):
    Aggregation: _AggregationSourceHelper
    Name: str | None = None
    NativeReferenceName: str | None = None  # only for Layout.Visual.Query

    def get_sources(self) -> list[DataSource]:
        return [self.Aggregation.Expression]


ScopedEvalExpression = Annotated[
    Annotated[DataSource, Tag("DataSource")]
    | Annotated[AggregationSource, Tag("AggregationSource")]
    | Annotated[SelectRef, Tag("SelectRef")],
    Discriminator(get_expression_type),
]
