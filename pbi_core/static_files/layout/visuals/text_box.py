from typing import Any

from attrs import field

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector
from pbi_core.static_files.layout.sources.paragraphs import Paragraph

from .base import BaseVisual
from .properties.base import Expression


class GeneralProperties(LayoutNode):
    class _GeneralPropertiesHelper(LayoutNode):
        paragraphs: list[Paragraph] | None = None
        responsive: Expression | None = None

    properties: _GeneralPropertiesHelper = field(factory=_GeneralPropertiesHelper)


class ValueProperties(LayoutNode):
    class _ValuePropertiesHelper(LayoutNode):
        class _ValuePropertiesExpr(LayoutNode):
            context: Any | None = None  # TODO: should be Source, but causes circular import issues with Subquery
            expr: Any | None = None  # TODO: should be Source, but causes circular import issues with Subquery
            value: Any | None = None  # TODO: should be Source, but causes circular import issues with Subquery
            propertyDefinitionKind: str | None = None

        expr: _ValuePropertiesExpr = field(factory=_ValuePropertiesExpr)
        formatString: Expression | None = None

    properties: _ValuePropertiesHelper = field(factory=_ValuePropertiesHelper)
    selector: Selector | None = None


class TextBoxProperties(LayoutNode):
    general: list[GeneralProperties] = field(factory=lambda: [GeneralProperties()])
    values: list[ValueProperties] = field(factory=lambda: [ValueProperties()])


class TextBox(BaseVisual):
    visualType: str = "textbox"

    drillFilterOtherVisuals: bool = True
    objects: TextBoxProperties = field(factory=TextBoxProperties)
