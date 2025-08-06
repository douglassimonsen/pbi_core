from typing import Any

from git import Optional
from pydantic import ConfigDict

from .._base_node import LayoutNode
from .base import BaseVisual
from .properties import Expression


class TitleProperties(LayoutNode):
    text: Optional[Expression] = None
    heading: Optional[Expression] = None
    fontFamily: Optional[Expression] = None
    fontColor: Optional[Expression] = None
    fontSize: Optional[Expression] = None
    alignment: Optional[Expression] = None
    show: Optional[Expression] = None


class TitlePropertiesGroup(LayoutNode):
    properties: TitleProperties


class VisualHeaderProperties(LayoutNode):
    showTooltipButton: Optional[Expression] = None
    showSmartNarrativeButton: Optional[Expression] = None
    showVisualInformationButton: Optional[Expression] = None
    showVisualWarningButton: Optional[Expression] = None

    show: Optional[Expression] = None
    background: Optional[Expression] = None
    transparency: Optional[Expression] = None
    foreground: Optional[Expression] = None
    showDrillRoleSelector: Optional[Expression] = None
    showFocusModeButton: Optional[Expression] = None
    showOptionsMenu: Optional[Expression] = None


class VisualHeadersPropertiesGroup(LayoutNode):
    properties: VisualHeaderProperties


class BarChartVCObjects(LayoutNode):
    background: Any = None
    general: Any = None
    title: list[TitlePropertiesGroup]
    visualHeader: Optional[list[VisualHeadersPropertiesGroup]] = None
    visualTooltip: Any = None


class BarChart(BaseVisual):
    visualType: str = "barChart"
    model_config = ConfigDict(extra="forbid")
    vcObjects: Optional[BarChartVCObjects] = None
    columnProperties: Any = None
