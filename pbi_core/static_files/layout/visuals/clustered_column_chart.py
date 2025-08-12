from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .properties.base import Expression


class LabelsPropertiesHelper(LayoutNode):
    fontSize: Expression | None = None
    labelDisplayUnits: Expression | None = None
    labelOverflow: Expression | None = None
    show: Expression | None = None


class LabelsProperties(LayoutNode):
    properties: LabelsPropertiesHelper
    selector: Selector | None = None


class ValueAxisPropertiesHelper(LayoutNode):
    axisScale: Expression | None = None
    show: Expression | None = None


class ValueAxisProperties(LayoutNode):
    properties: ValueAxisPropertiesHelper
    selector: Selector | None = None


class DataPointPropertiesHelper(LayoutNode):
    fill: Expression | None = None


class DataPointProperties(LayoutNode):
    properties: DataPointPropertiesHelper


class ClusteredColumnChartProperties(LayoutNode):
    dataPoint: list[DataPointProperties] | None = None
    labels: list[LabelsProperties] | None = None
    valueAxis: list[ValueAxisProperties] | None = None


class ClusteredColumnChart(BaseVisual):
    visualType: str = "clusteredColumnChart"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: ClusteredColumnChartProperties | None = None
