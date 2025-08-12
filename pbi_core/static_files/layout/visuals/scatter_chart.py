from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .column_property import ColumnProperty
from .properties.base import Expression


class DataPointPropertiesHelper(LayoutNode):
    fill: Expression | None = None
    fillRule: Expression | None = None
    legend: Expression | None = None
    valueAxis: Expression | None = None


class DataPointProperties(LayoutNode):
    properties: DataPointPropertiesHelper
    selector: Selector | None = None


class ValueAxisPropertiesHelper(LayoutNode):
    show: Expression | None = None
    alignZeros: Expression | None = None


class ValueAxisProperties(LayoutNode):
    properties: ValueAxisPropertiesHelper


class LegendPropertiesHelper(LayoutNode):
    show: Expression | None = None


class LegendProperties(LayoutNode):
    properties: LegendPropertiesHelper


class ScatterChartProperties(LayoutNode):
    dataPoint: list[DataPointProperties] | None = None
    legend: list[LegendProperties] | None = None
    valueAxis: list[ValueAxisProperties] | None = None


class ScatterChart(BaseVisual):
    visualType: str = "scatterChart"
    model_config = ConfigDict(extra="forbid")

    columnProperties: dict[str, ColumnProperty] | None = None
    drillFilterOtherVisuals: bool = True
    objects: ScatterChartProperties | None = None
