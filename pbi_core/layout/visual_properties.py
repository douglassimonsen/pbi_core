import inspect
from typing import TYPE_CHECKING, Optional

from pydantic import ConfigDict

from ._base_node import LayoutNode
from .sources import LiteralSource

if TYPE_CHECKING:
    from .visual import SingleVisual


class LiteralExpression(LayoutNode):
    expr: LiteralSource


class SingleVisualObjectProperties(LayoutNode):
    model_config = ConfigDict(extra="allow")


class GeneralPropertiesHelper(LayoutNode):
    keepLayerOrder: Optional[LiteralExpression] = None
    altText: Optional[LiteralExpression] = None


class GeneralProperties(LayoutNode):
    parent: "SingleVisualVCObjects"
    properties: GeneralPropertiesHelper


class SingleVisualVCObjects(LayoutNode):
    parent: "SingleVisual"
    model_config = ConfigDict(extra="allow")

    background: Optional[list[SingleVisualObjectProperties]] = None
    border: Optional[list[SingleVisualObjectProperties]] = None
    divider: Optional[list[SingleVisualObjectProperties]] = None
    general: Optional[list[GeneralProperties]] = None
    padding: Optional[list[SingleVisualObjectProperties]] = None
    spacing: Optional[list[SingleVisualObjectProperties]] = None
    subTitle: Optional[list[SingleVisualObjectProperties]] = None
    title: Optional[list[SingleVisualObjectProperties]] = None
    visualTooltip: Optional[list[SingleVisualObjectProperties]] = None


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
