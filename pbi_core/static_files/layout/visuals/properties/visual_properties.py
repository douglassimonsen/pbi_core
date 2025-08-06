import inspect
from typing import Annotated, Any, Union, cast

from pydantic import Discriminator, Tag

from ..._base_node import LayoutNode
from ...sources import LiteralSource, MeasureSource


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
    expr: ThemeExpression


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
    return cast(str, v.__class__.__name__)


Expression = Annotated[
    Union[
        Annotated[LiteralExpression, Tag("LiteralExpression")],
        Annotated[MeasureExpression, Tag("MeasureExpression")],
        Annotated[SolidColorExpression, Tag("SolidColorExpression")],
    ],
    Discriminator(get_expression),
]

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
