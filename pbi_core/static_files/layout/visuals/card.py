from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .column_property import ColumnProperty
from .properties.base import Expression


class CategoryLabelsProperties(LayoutNode):
    class _CategoryLabelsPropertiesHelper(LayoutNode):
        color: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        show: Expression | None = None

    properties: _CategoryLabelsPropertiesHelper
    selector: Selector | None = None


class LabelsProperties(LayoutNode):
    class _LabelsPropertiesHelper(LayoutNode):
        color: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        labelPrecision: Expression | None = None
        labelDisplayUnits: Expression | None = None
        preserveWhitespace: Expression | None = None

    properties: _LabelsPropertiesHelper
    selector: Selector | None = None


class GeneralProperties(LayoutNode):
    class _GeneralPropertiesHelper(LayoutNode):
        pass

    properties: _GeneralPropertiesHelper


class WordWrapProperties(LayoutNode):
    class _WordWrapperPropertiesHelper(LayoutNode):
        show: Expression | None = None

    properties: _WordWrapperPropertiesHelper


class CardProperties(LayoutNode):
    categoryLabels: list[CategoryLabelsProperties] | None = None
    general: list[GeneralProperties] | None = None
    labels: list[LabelsProperties] | None = None
    wordWrap: list[WordWrapProperties] | None = None


class Card(BaseVisual):
    visualType: str = "card"
    model_config = ConfigDict(extra="forbid")

    columnProperties: dict[str, ColumnProperty] | None = None
    drillFilterOtherVisuals: bool = True
    objects: CardProperties | None = None
