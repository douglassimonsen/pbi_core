from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .column_property import ColumnProperty
from .properties.base import Expression


class DataPointPropertiesHelper(LayoutNode):
    fill: Expression | None = None
    fillRule: Expression | None = None


class DataPointProperties(LayoutNode):
    properties: DataPointPropertiesHelper
    selector: Selector | None = None


class LabelsPropertiesHelper(LayoutNode):
    backgroundColor: Expression | None = None
    backgroundTransparency: Expression | None = None
    enableBackground: Expression | None = None
    fontSize: Expression | None = None
    labelOrientation: Expression | None = None
    labelPosition: Expression | None = None
    show: Expression | None = None


class LabelsProperties(LayoutNode):
    properties: LabelsPropertiesHelper
    selector: Selector | None = None


class LegendPropertiesHelper(LayoutNode):
    legendMarkerRendering: Expression | None = None


class LegendProperties(LayoutNode):
    properties: LegendPropertiesHelper
    selector: Selector | None = None


class LineStylesPropertiesHelper(LayoutNode):
    lineStyle: Expression | None = None
    markerShape: Expression | None = None
    showMarker: Expression | None = None
    showSeries: Expression | None = None
    strokeWidth: Expression | None = None


class LineStylesProperties(LayoutNode):
    properties: LineStylesPropertiesHelper
    selector: Selector | None = None


class ValueAxisPropertiesHelper(LayoutNode):
    alignZeros: Expression | None = None
    gridlineShow: Expression | None = None
    secEnd: Expression | None = None
    secStart: Expression | None = None
    show: Expression | None = None


class ValueAxisProperties(LayoutNode):
    properties: ValueAxisPropertiesHelper
    selector: Selector | None = None


class LineStackedColumnComboChartProperties(LayoutNode):
    dataPoint: list[DataPointProperties] | None = None
    labels: list[LabelsProperties] | None = None
    legend: list[LegendProperties] | None = None
    lineStyles: list[LineStylesProperties] | None = None
    valueAxis: list[ValueAxisProperties] | None = None


class LineStackedColumnComboChart(BaseVisual):
    visualType: str = "lineStackedColumnComboChart"
    model_config = ConfigDict(extra="forbid")

    columnProperties: dict[str, ColumnProperty] | None = None
    drillFilterOtherVisuals: bool = True
    objects: LineStackedColumnComboChartProperties | None = None
