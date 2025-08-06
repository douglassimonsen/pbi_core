# ruff: noqa: N815
from typing import TYPE_CHECKING

from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode

from .basic_shape import GeneralProperties

if TYPE_CHECKING:
    from pbi_core.static_files.model_references import ModelColumnReference, ModelMeasureReference


class TextStyle(LayoutNode):
    color: str  # TODO: check that it's hex
    fontSize: str


class TextRun(LayoutNode):
    textStyle: TextStyle
    value: str


class Paragraph(LayoutNode):
    horizontalTextAlignment: str  # TODO: convert to enum
    textRuns: list[TextRun]


class GeneralProperties(LayoutNode):
    paragraphs: list[Paragraph] | None = None


class General(LayoutNode):
    properties: GeneralProperties


class TextBoxProperties(LayoutNode):
    general: list[General]


class TextBox(LayoutNode):
    visualType: str = "textbox"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: TextBoxProperties | None = None

    def get_ssas_elements(self) -> "set[ModelColumnReference | ModelMeasureReference]":  # noqa: PLR6301
        return set()
