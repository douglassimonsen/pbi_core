from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .properties.base import Expression


class FillPropertiesHelper(LayoutNode):
    show: Expression | None = None


class FillProperties(LayoutNode):
    properties: FillPropertiesHelper


class IconPropertiesHelper(LayoutNode):
    bottomMargin: Expression | None = None
    horizontalAlignment: Expression | None = None
    leftMargin: Expression | None = None
    lineColor: Expression | None = None
    lineWeight: Expression | None = None
    rightMargin: Expression | None = None
    shapeType: Expression | None = None
    show: Expression | None = None
    topMargin: Expression | None = None


class IconProperties(LayoutNode):
    properties: IconPropertiesHelper
    selector: Selector | None = None


class TextPropertiesHelper(LayoutNode):
    fontColor: Expression | None = None
    fontSize: Expression | None = None
    horizontalAlignment: Expression | None = None
    rightMargin: Expression | None = None
    show: Expression | None = None
    text: Expression | None = None
    topMargin: Expression | None = None
    verticalAlignment: Expression | None = None


class TextProperties(LayoutNode):
    properties: TextPropertiesHelper
    selector: Selector | None = None


class ActionButtonProperties(LayoutNode):
    fill: list[FillProperties] | None = None
    icon: list[IconProperties] | None = None
    text: list[TextProperties] | None = None


class ActionButton(BaseVisual):
    visualType: str = "actionButton"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: ActionButtonProperties | None = None
