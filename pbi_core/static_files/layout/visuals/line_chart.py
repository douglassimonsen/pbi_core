from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .properties.base import Expression


class CategoryAxisPropertiesHelper(LayoutNode):
    concatenateLabels: Expression | None = None


class CategoryAxisProperties(LayoutNode):
    properties: CategoryAxisPropertiesHelper
    selector: Selector | None = None


class LineStylesPropertiesHelper(LayoutNode):
    markerShape: Expression | None = None
    showMarker: Expression | None = None
    showSeries: Expression | None = None
    strokeWidth: Expression | None = None


class LineStylesProperties(LayoutNode):
    properties: LineStylesPropertiesHelper
    selector: Selector | None = None


class LineChartProperties(LayoutNode):
    categoryAxis: list[CategoryAxisProperties] | None = None
    lineStyles: list[LineStylesProperties] | None = None


class LineChart(BaseVisual):
    visualType: str = "lineChart"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: LineChartProperties | None = None
