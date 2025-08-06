from typing import Annotated, Any, cast

from pydantic import Discriminator, Tag

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.sources import LiteralSource, MeasureSource


class LiteralExpression(LayoutNode):
    expr: LiteralSource


class MeasureExpression(LayoutNode):
    expr: MeasureSource


class ThemeDataColor(LayoutNode):
    ColorId: int
    Percent: int


class ThemeExpression(LayoutNode):
    ThemeDataColor: ThemeDataColor


class ColorExpression(LayoutNode):
    expr: ThemeExpression | LiteralSource


class SolidExpression(LayoutNode):
    color: ColorExpression


class SolidColorExpression(LayoutNode):
    solid: SolidExpression


def get_expression(v: Any) -> str:
    if isinstance(v, dict):
        if "solid" in v:
            return "SolidColorExpression"
        if "Measure" in v["expr"]:
            return "MeasureExpression"
        if "Literal" in v["expr"]:
            return "LiteralExpression"
        raise ValueError
    return cast("str", v.__class__.__name__)


Expression = Annotated[
    Annotated[LiteralExpression, Tag("LiteralExpression")]
    | Annotated[MeasureExpression, Tag("MeasureExpression")]
    | Annotated[SolidColorExpression, Tag("SolidColorExpression")],
    Discriminator(get_expression),
]
