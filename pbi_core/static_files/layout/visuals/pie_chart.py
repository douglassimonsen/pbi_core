from attrs import field

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .properties.base import Expression


class DataPointProperties(LayoutNode):
    class _DataPointPropertiesHelper(LayoutNode):
        fill: Expression | None = None
        showAllDataPoints: Expression | None = None

    properties: _DataPointPropertiesHelper = field(factory=_DataPointPropertiesHelper)
    selector: Selector | None = None


class LabelsProperties(LayoutNode):
    class _LabelsPropertiesHelper(LayoutNode):
        color: Expression | None = None
        labelDisplayUnits: Expression | None = None
        labelPrecision: Expression | None = None
        labelStyle: Expression | None = None
        percentageLabelPrecision: Expression | None = None
        show: Expression | None = None

    properties: _LabelsPropertiesHelper = field(factory=_LabelsPropertiesHelper)


class LegendProperties(LayoutNode):
    class _LegendPropertiesHelper(LayoutNode):
        position: Expression | None = None
        show: Expression | None = None

    properties: _LegendPropertiesHelper = field(factory=_LegendPropertiesHelper)


class PieChartProperties(LayoutNode):
    dataPoint: list[DataPointProperties] = field(factory=lambda: [DataPointProperties()])
    labels: list[LabelsProperties] = field(factory=lambda: [LabelsProperties()])
    legend: list[LegendProperties] = field(factory=lambda: [LegendProperties()])


class PieChart(BaseVisual):
    visualType: str = "pieChart"
    objects: PieChartProperties = field(factory=PieChartProperties)
