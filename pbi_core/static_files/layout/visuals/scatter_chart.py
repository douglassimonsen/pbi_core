from attrs import field

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .properties.base import Expression


class BubblesProperties(LayoutNode):
    class _BubblesPropertiesHelper(LayoutNode):
        bubbleSize: Expression | None = None
        markerShape: Expression | None = None
        showSeries: Expression | None = None

    properties: _BubblesPropertiesHelper = field(factory=_BubblesPropertiesHelper)
    selector: Selector | None = None


class CategoryAxisProperties(LayoutNode):
    class _CategoryAxisPropertiesHelper(LayoutNode):
        axisScale: Expression | None = None
        end: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        gridlineColor: Expression | None = None
        gridlineShow: Expression | None = None
        gridlineStyle: Expression | None = None
        innerPadding: Expression | None = None
        labelColor: Expression | None = None
        logAxisScale: Expression | None = None
        maxMarginFactor: Expression | None = None
        show: Expression | None = None
        showAxisTitle: Expression | None = None
        start: Expression | None = None
        titleColor: Expression | None = None
        titleFontFamily: Expression | None = None
        titleFontSize: Expression | None = None
        titleText: Expression | None = None
        treatNullsAsZero: Expression | None = None

    properties: _CategoryAxisPropertiesHelper = field(factory=_CategoryAxisPropertiesHelper)


class CategoryLabelsProperties(LayoutNode):
    class _CategoryLabelsPropertiesHelper(LayoutNode):
        color: Expression | None = None
        enableBackground: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        show: Expression | None = None

    properties: _CategoryLabelsPropertiesHelper = field(factory=_CategoryLabelsPropertiesHelper)


class ColorBorderProperties(LayoutNode):
    class _ColorBorderPropertiesHelper(LayoutNode):
        show: Expression | None = None

    properties: _ColorBorderPropertiesHelper = field(factory=_ColorBorderPropertiesHelper)


class DataPointProperties(LayoutNode):
    class _DataPointPropertiesHelper(LayoutNode):
        fill: Expression | None = None
        fillRule: Expression | None = None
        legend: Expression | None = None
        showAllDataPoints: Expression | None = None
        valueAxis: Expression | None = None

    properties: _DataPointPropertiesHelper = field(factory=_DataPointPropertiesHelper)
    selector: Selector | None = None


class FillPointProperties(LayoutNode):
    class _FillPointPropertiesHelper(LayoutNode):
        show: Expression | None = None
        style: Expression | None = None

    properties: _FillPointPropertiesHelper = field(factory=_FillPointPropertiesHelper)


class GeneralProperties(LayoutNode):
    class _GeneralPropertiesHelper(LayoutNode):
        responsive: Expression | None = None

    properties: _GeneralPropertiesHelper = field(factory=_GeneralPropertiesHelper)


class LegendProperties(LayoutNode):
    class _LegendPropertiesHelper(LayoutNode):
        fontSize: Expression | None = None
        labelColor: Expression | None = None
        position: Expression | None = None
        show: Expression | None = None
        showGradientLegend: Expression | None = None
        showTitle: Expression | None = None
        titleText: Expression | None = None

    properties: _LegendPropertiesHelper = field(factory=_LegendPropertiesHelper)


class PlotAreaProperties(LayoutNode):
    class _PlotAreaPropertiesHelper(LayoutNode):
        transparency: Expression | None = None

    properties: _PlotAreaPropertiesHelper = field(factory=_PlotAreaPropertiesHelper)


class ValueAxisProperties(LayoutNode):
    class _ValueAxisPropertiesHelper(LayoutNode):
        alignZeros: Expression | None = None
        axisScale: Expression | None = None
        end: Expression | None = None
        fontSize: Expression | None = None
        gridlineColor: Expression | None = None
        gridlineShow: Expression | None = None
        labelColor: Expression | None = None
        logAxisScale: Expression | None = None
        show: Expression | None = None
        showAxisTitle: Expression | None = None
        start: Expression | None = None
        switchAxisPosition: Expression | None = None
        titleColor: Expression | None = None
        titleFontFamily: Expression | None = None
        titleFontSize: Expression | None = None
        titleText: Expression | None = None
        treatNullsAsZero: Expression | None = None

    properties: _ValueAxisPropertiesHelper = field(factory=_ValueAxisPropertiesHelper)


class Y1AxisReferenceLineProperties(LayoutNode):
    class _Y1AxisReferenceLinePropertiesHelper(LayoutNode):
        displayName: Expression | None = None
        lineColor: Expression | None = None
        show: Expression | None = None
        value: Expression | None = None

    properties: _Y1AxisReferenceLinePropertiesHelper = field(factory=_Y1AxisReferenceLinePropertiesHelper)
    selector: Selector | None = None


class ScatterChartProperties(LayoutNode):
    bubbles: list[BubblesProperties] = field(factory=lambda: [BubblesProperties()])
    categoryAxis: list[CategoryAxisProperties] = field(factory=lambda: [CategoryAxisProperties()])
    categoryLabels: list[CategoryLabelsProperties] = field(factory=lambda: [CategoryLabelsProperties()])
    colorBorder: list[ColorBorderProperties] = field(factory=lambda: [ColorBorderProperties()])
    dataPoint: list[DataPointProperties] = field(factory=lambda: [DataPointProperties()])
    fillPoint: list[FillPointProperties] = field(factory=lambda: [FillPointProperties()])
    general: list[GeneralProperties] = field(factory=lambda: [GeneralProperties()])
    legend: list[LegendProperties] = field(factory=lambda: [LegendProperties()])
    plotArea: list[PlotAreaProperties] = field(factory=lambda: [PlotAreaProperties()])
    valueAxis: list[ValueAxisProperties] = field(factory=lambda: [ValueAxisProperties()])
    y1AxisReferenceLine: list[Y1AxisReferenceLineProperties] = field(
        factory=lambda: [Y1AxisReferenceLineProperties()],
    )


class ScatterChart(BaseVisual):
    visualType: str = "scatterChart"

    drillFilterOtherVisuals: bool = True
    objects: ScatterChartProperties = field(factory=ScatterChartProperties)
