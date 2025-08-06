from typing import Annotated, Any

from pydantic import Discriminator, Tag

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.sources import LiteralSource, MeasureSource, Source

from ...sources.aggregation import AggregationSource


class LiteralExpression(LayoutNode):
    expr: LiteralSource


class MeasureExpression(LayoutNode):
    expr: MeasureSource


class ThemeDataColor(LayoutNode):
    ColorId: int
    Percent: float


class ThemeExpression(LayoutNode):
    ThemeDataColor: ThemeDataColor


class FillRule(LayoutNode):
    FillRule: "Expression"
    Input: Source


class FillRuleExpression(LayoutNode):
    FillRule: FillRule


def get_subexpr_type(v: object | dict[str, Any]) -> str:
    if isinstance(v, dict):
        if "ThemeDataColor" in v:
            return "ThemeExpression"
        if "Aggregation" in v:
            return "AggregationSource"
        if "Literal" in v:
            return "LiteralSource"
        if "Measure" in v:
            return "MeasureSource"
        if "FillRule" in v:
            return "FillRuleExpression"
        msg = f"Unknown type: {v.keys()}"
        raise TypeError(msg)
    return v.__class__.__name__


ColorSubExpression = Annotated[
    Annotated[ThemeExpression, Tag("ThemeExpression")]
    | Annotated[LiteralSource, Tag("LiteralSource")]
    | Annotated[MeasureSource, Tag("MeasureSource")]
    | Annotated[FillRuleExpression, Tag("FillRuleExpression")]
    | Annotated[AggregationSource, Tag("AggregationSource")],
    Discriminator(get_subexpr_type),
]


class ColorExpression(LayoutNode):
    expr: ColorSubExpression


def get_color_type(v: object | dict[str, Any]) -> str:
    if isinstance(v, dict):
        if "expr" in v:
            return "ColorExpression"
        if "Literal" in v:
            return "LiteralSource"
        msg = f"Unknown Color Type: {v.keys()}"
        raise TypeError(msg)
    return v.__class__.__name__


Color = Annotated[
    Annotated[ColorExpression, Tag("ColorExpression")] | Annotated[LiteralSource, Tag("LiteralSource")],
    Discriminator(get_color_type),
]


class SolidExpression(LayoutNode):
    color: Color


class SolidColorExpression(LayoutNode):
    solid: SolidExpression


class StrategyExpression(LayoutNode):
    strategy: LiteralExpression | LiteralSource  # TODO: explore the cases here more


class LinearGradient2Helper(LayoutNode):
    max: SolidExpression
    min: SolidExpression
    nullColoringStrategy: StrategyExpression


class LinearGradient2Expression(LayoutNode):
    linearGradient2: LinearGradient2Helper


class LinearGradient3Helper(LayoutNode):
    max: SolidExpression
    mid: SolidExpression
    min: SolidExpression
    nullColoringStrategy: StrategyExpression


class LinearGradient3Expression(LayoutNode):
    linearGradient3: LinearGradient3Helper


def get_expression(v: object | dict[str, Any]) -> str:
    if isinstance(v, dict):
        if "solid" in v:
            return "SolidColorExpression"
        if "linearGradient2" in v:
            return "LinearGradient2Expression"
        if "linearGradient3" in v:
            return "LinearGradient3Expression"

        if "expr" not in v:
            raise ValueError(f"Unknown Expression: {v.keys()}")
        if "Measure" in v["expr"]:
            return "MeasureExpression"
        if "Literal" in v["expr"]:
            return "LiteralExpression"
        raise ValueError
    return v.__class__.__name__


Expression = Annotated[
    Annotated[LiteralExpression, Tag("LiteralExpression")]
    | Annotated[MeasureExpression, Tag("MeasureExpression")]
    | Annotated[SolidColorExpression, Tag("SolidColorExpression")]
    | Annotated[LinearGradient2Expression, Tag("LinearGradient2Expression")]
    | Annotated[LinearGradient3Expression, Tag("LinearGradient3Expression")],
    Discriminator(get_expression),
]
