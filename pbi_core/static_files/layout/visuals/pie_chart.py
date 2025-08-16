from pydantic import ConfigDict, Field

from pbi_core.static_files.layout._base_node import LayoutNode

from ..selector import Selector
from .base import BaseVisual
from .column_property import ColumnProperty
from .properties.base import Expression


class LegendProperties(LayoutNode):
    class _LegendPropertiesHelper(LayoutNode):
        position: Expression | None = None
        show: Expression | None = None

    properties: _LegendPropertiesHelper = Field(default_factory=_LegendPropertiesHelper)


class DataPointProperties(LayoutNode):
    class _DataPointPropertiesHelper(LayoutNode):
        fill: Expression | None = None
        showAllDataPoints: Expression | None = None

    properties: _DataPointPropertiesHelper = Field(default_factory=_DataPointPropertiesHelper)
    selector: Selector | None = None


class LabelsProperties(LayoutNode):
    class _LabelsPropertiesHelper(LayoutNode):
        color: Expression | None = None
        labelDisplayUnits: Expression | None = None
        labelPrecision: Expression | None = None
        labelStyle: Expression | None = None
        percentageLabelPrecision: Expression | None = None
        show: Expression | None = None

    properties: _LabelsPropertiesHelper = Field(default_factory=_LabelsPropertiesHelper)


class PieChartProperties(LayoutNode):
    dataPoint: list[DataPointProperties] | None = Field(default_factory=list[DataPointProperties()])
    labels: list[LabelsProperties] | None = Field(default_factory=list[LabelsProperties()])
    legend: list[LegendProperties] | None = Field(default_factory=list[LegendProperties()])


class PieChart(BaseVisual):
    visualType: str = "pieChart"
    model_config = ConfigDict(extra="forbid")
    columnProperties: dict[str, ColumnProperty] | None = None
    objects: PieChartProperties | None = Field(default_factory=PieChartProperties)
