from typing import Annotated, Any

from pydantic import Discriminator, Tag

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.sources import LiteralSource, MeasureSource


class LiteralExpression(LayoutNode):
    expr: LiteralSource


class MeasureExpression(LayoutNode):
    expr: MeasureSource


class ThemeDataColor(LayoutNode):
    ColorId: int
    Percent: float


class ThemeExpression(LayoutNode):
    ThemeDataColor: ThemeDataColor


def get_subexpr_type(v: object | dict[str, Any]) -> str:
    if isinstance(v, dict):
        if "ThemeDataColor" in v:
            return "ThemeExpression"
        if "Literal" in v:
            return "LiteralSource"
        if "Measure" in v:
            return "MeasureSource"
    return v.__class__.__name__


ColorSubExpression = Annotated[
    Annotated[ThemeExpression, Tag("ThemeExpression")]
    | Annotated[LiteralSource, Tag("LiteralSource")]
    | Annotated[MeasureSource, Tag("MeasureSource")],
    Discriminator(get_subexpr_type),
]


class ColorExpression(LayoutNode):
    expr: ColorSubExpression


class SolidExpression(LayoutNode):
    color: ColorExpression


class SolidColorExpression(LayoutNode):
    solid: SolidExpression


class StrategyExpression(LayoutNode):
    strategy: LiteralExpression


class LinearGradient2Helper(LayoutNode):
    max: SolidExpression
    min: SolidExpression
    nullColoringStrategy: StrategyExpression


class LinearGradient2Expression(LayoutNode):
    linearGradient2: LinearGradient2Helper


def get_expression(v: object | dict[str, Any]) -> str:
    if isinstance(v, dict):
        if "solid" in v:
            return "SolidColorExpression"
        if "linearGradient2" in v:
            return "LinearGradient2Expression"
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
    | Annotated[LinearGradient2Expression, Tag("LinearGradient2Expression")],
    Discriminator(get_expression),
]
