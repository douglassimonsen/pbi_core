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


class TitlePropertiesGroup(LayoutNode):
    properties: TitleProperties


class VisualHeaderProperties(LayoutNode):
    showTooltipButton: Expression
    showSmartNarrativeButton: Expression
    showVisualInformationButton: Expression
    showVisualWarningButton: Expression


class VisualHeadersPropertiesGroup(LayoutNode):
    properties: VisualHeaderProperties


class BarChartVCObjects(LayoutNode):
    title: list[TitlePropertiesGroup]
    visualHeader: list[VisualHeadersPropertiesGroup]


class BarChart(BaseVisual):
    visualType: str = "barChart"
    model_config = ConfigDict(extra="forbid")
    vcObjects: Optional[BarChartVCObjects] = None
    columnProperties: Any = None
