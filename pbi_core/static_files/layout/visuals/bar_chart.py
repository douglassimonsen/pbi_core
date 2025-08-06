# ruff: noqa: N815
from typing import Any

from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode

from .base import BaseVisual
from .properties import Expression


class TitleProperties(LayoutNode):
    text: Expression | None = None
    heading: Expression | None = None
    fontFamily: Expression | None = None
    fontColor: Expression | None = None
    fontSize: Expression | None = None
    alignment: Expression | None = None
    show: Expression | None = None
    titleWrap: Expression | None = None
    background: Expression | None = None


class TitlePropertiesGroup(LayoutNode):
    properties: TitleProperties


class BorderProperties(LayoutNode):
    show: Expression | None = None
    background: Expression | None = None
    color: Expression | None = None
    radius: Expression | None = None


class BorderPropertiesGroup(LayoutNode):
    properties: BorderProperties


class VisualHeaderProperties(LayoutNode):
    showTooltipButton: Expression | None = None
    showSmartNarrativeButton: Expression | None = None
    showVisualInformationButton: Expression | None = None
    showVisualWarningButton: Expression | None = None

    show: Expression | None = None
    background: Expression | None = None
    transparency: Expression | None = None
    foreground: Expression | None = None
    showDrillRoleSelector: Expression | None = None
    showFocusModeButton: Expression | None = None
    showOptionsMenu: Expression | None = None
    showVisualErrorButton: Expression | None = None
    showDrillUpButton: Expression | None = None
    showDrillToggleButton: Expression | None = None
    showDrillDownLevelButton: Expression | None = None
    showDrillDownExpandButton: Expression | None = None
    showSeeDataLayoutToggleButton: Expression | None = None
    showFilterRestatementButton: Expression | None = None
    showPinButton: Expression | None = None


class VisualHeadersPropertiesGroup(LayoutNode):
    properties: VisualHeaderProperties


# TODO: remove Anys
class BarChartVCObjects(LayoutNode):
    background: Any = None
    general: Any = None
    title: list[TitlePropertiesGroup] = []
    visualHeader: list[VisualHeadersPropertiesGroup] | None = None
    visualTooltip: Any = None
    border: list[BorderPropertiesGroup] | None = None
    visualHeaderTooltip: Any = None


class BarChart(BaseVisual):
    visualType: str = "barChart"
    model_config = ConfigDict(extra="forbid")
    vcObjects: BarChartVCObjects | None = None
    columnProperties: Any = None
