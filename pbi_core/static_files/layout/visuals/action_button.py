from pydantic import ConfigDict, Field

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .properties.base import Expression


class FillPropertiesHelper(LayoutNode):
    fillColor: Expression | None = None
    image: Expression | None = None
    show: Expression | None = None
    transparency: Expression | None = None


class FillProperties(LayoutNode):
    properties: FillPropertiesHelper = Field(default_factory=FillPropertiesHelper)
    selector: Selector | None = None


class IconPropertiesHelper(LayoutNode):
    bottomMargin: Expression | None = None
    horizontalAlignment: Expression | None = None
    leftMargin: Expression | None = None
    lineColor: Expression | None = None
    lineTransparency: Expression | None = None
    lineWeight: Expression | None = None
    padding: Expression | None = None
    rightMargin: Expression | None = None
    shapeType: Expression | None = None
    show: Expression | None = None
    topMargin: Expression | None = None
    verticalAlignment: Expression | None = None


class IconProperties(LayoutNode):
    properties: IconPropertiesHelper = Field(default_factory=IconPropertiesHelper)
    selector: Selector | None = None


class TextPropertiesHelper(LayoutNode):
    fontColor: Expression | None = None
    fontFamily: Expression | None = None
    fontSize: Expression | None = None
    horizontalAlignment: Expression | None = None
    leftMargin: Expression | None = None
    padding: Expression | None = None
    rightMargin: Expression | None = None
    show: Expression | None = None
    text: Expression | None = None
    topMargin: Expression | None = None
    verticalAlignment: Expression | None = None


class TextProperties(LayoutNode):
    properties: TextPropertiesHelper = Field(default_factory=TextPropertiesHelper)
    selector: Selector | None = None


class OutlinePropertiesHelper(LayoutNode):
    lineColor: Expression | None = None
    roundEdge: Expression | None = None
    show: Expression | None = None
    transparency: Expression | None = None
    weight: Expression | None = None


class OutlineProperties(LayoutNode):
    properties: OutlinePropertiesHelper = Field(default_factory=OutlinePropertiesHelper)
    selector: Selector | None = None


class ShapeProperties(LayoutNode):
    class _ShapePropertiesHelper(LayoutNode):
        roundEdge: Expression | None = None

    properties: _ShapePropertiesHelper = Field(default_factory=_ShapePropertiesHelper)
    selector: Selector | None = None


class ActionButtonProperties(LayoutNode):
    fill: list[FillProperties] | None = Field(default_factory=lambda: [FillProperties()])
    icon: list[IconProperties] | None = Field(default_factory=lambda: [IconProperties()])
    outline: list[OutlineProperties] | None = Field(default_factory=lambda: [OutlineProperties()])
    shape: list[ShapeProperties] | None = Field(default_factory=lambda: [ShapeProperties()])
    text: list[TextProperties] | None = Field(default_factory=lambda: [TextProperties()])


class ActionButton(BaseVisual):
    visualType: str = "actionButton"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: ActionButtonProperties | None = None
