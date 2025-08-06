# ruff: noqa: N815
from typing import TYPE_CHECKING

from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode

from .properties.base import Expression

if TYPE_CHECKING:
    from pbi_core.static_files.model_references import ModelColumnReference, ModelMeasureReference


class FillPropertiesHelper(LayoutNode):
    fillColor: Expression | None = None
    transparency: Expression | None = None
    show: Expression | None = None


class FillProperties(LayoutNode):
    properties: FillPropertiesHelper


class GeneralPropertiesHelper(LayoutNode):
    shapeType: Expression | None = None


class GeneralProperties(LayoutNode):
    properties: GeneralPropertiesHelper


class LinePropertiesHelper(LayoutNode):
    lineColor: Expression | None = None
    transparency: Expression | None = None


class LineProperties(LayoutNode):
    properties: LinePropertiesHelper


class BasicShapeProperties(LayoutNode):
    fill: list[FillProperties]
    general: list[GeneralProperties]
    line: list[LineProperties]


class BasicShape(LayoutNode):
    visualType: str = "basicShape"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: BasicShapeProperties | None = None
    vcObjects: int = None
    display: int = None

    def get_ssas_elements(self) -> "set[ModelColumnReference | ModelMeasureReference]":  # noqa: PLR6301
        return set()
