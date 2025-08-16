from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .column_property import ColumnProperty
from .properties.base import Expression


class LabelsProperties(LayoutNode):
    class _LabelsPropertiesHelper(LayoutNode):
        backgroundTransparency: Expression | None = None
        color: Expression | None = None
        enableBackground: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        labelDisplayUnits: Expression | None = None
        labelOrientation: Expression | None = None
        labelOverflow: Expression | None = None
        labelPosition: Expression | None = None
        labelPrecision: Expression | None = None
        show: Expression | None = None
        showAll: Expression | None = None

    properties: _LabelsPropertiesHelper
    selector: Selector | None = None


class ValueAxisProperties(LayoutNode):
    class _ValueAxisPropertiesHelper(LayoutNode):
        axisScale: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        gridlineShow: Expression | None = None
        labelColor: Expression | None = None
        labelDisplayUnits: Expression | None = None
        logAxisScale: Expression | None = None
        show: Expression | None = None
        showAxisTitle: Expression | None = None
        start: Expression | None = None
        titleFontFamily: Expression | None = None

    properties: _ValueAxisPropertiesHelper
    selector: Selector | None = None


class DataPointProperties(LayoutNode):
    class _DataPointPropertiesHelper(LayoutNode):
        fill: Expression | None = None
        showAllDataPoints: Expression | None = None

    properties: _DataPointPropertiesHelper
    selector: Selector | None = None


class CategoryAxisProperties(LayoutNode):
    class _CategoryAxisPropertiesHelper(LayoutNode):
        axisType: Expression | None = None
        concatenateLabels: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        gridlineShow: Expression | None = None
        gridlineStyle: Expression | None = None
        innerPadding: Expression | None = None
        labelColor: Expression | None = None
        maxMarginFactor: Expression | None = None
        preferredCategoryWidth: Expression | None = None
        show: Expression | None = None
        showAxisTitle: Expression | None = None
        titleColor: Expression | None = None
        titleFontSize: Expression | None = None

    properties: _CategoryAxisPropertiesHelper


class LegendProperties(LayoutNode):
    class _LegendPropertiesHelper(LayoutNode):
        fontSize: Expression | None = None
        labelColor: Expression | None = None
        position: Expression | None = None
        show: Expression | None = None
        showTitle: Expression | None = None

    properties: _LegendPropertiesHelper


class TrendProperties(LayoutNode):
    class _TrendPropertiesHelper(LayoutNode):
        displayName: Expression | None = None
        lineColor: Expression | None = None
        show: Expression | None = None

    properties: _TrendPropertiesHelper


class PlotAreaProperties(LayoutNode):
    class _PlotAreaPropertiesHelper(LayoutNode):
        transparency: Expression | None = None

    properties: _PlotAreaPropertiesHelper


class GeneralProperties(LayoutNode):
    class _GeneralPropertiesHelper(LayoutNode):
        responsive: Expression | None = None

    properties: _GeneralPropertiesHelper


class ClusteredColumnChartProperties(LayoutNode):
    categoryAxis: list[CategoryAxisProperties] | None = None
    dataPoint: list[DataPointProperties] | None = None
    general: list[GeneralProperties] | None = None
    labels: list[LabelsProperties] | None = None
    legend: list[LegendProperties] | None = None
    plotArea: list[PlotAreaProperties] | None = None
    trend: list[TrendProperties] | None = None
    valueAxis: list[ValueAxisProperties] | None = None


class ClusteredColumnChart(BaseVisual):
    visualType: str = "clusteredColumnChart"
    model_config = ConfigDict(extra="forbid")

    columnProperties: dict[str, ColumnProperty] | None = None
    drillFilterOtherVisuals: bool = True
    objects: ClusteredColumnChartProperties | None = None
