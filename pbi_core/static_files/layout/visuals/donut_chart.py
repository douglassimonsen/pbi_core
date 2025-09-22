from attrs import field

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .properties.base import Expression


class BackgroundProperties(LayoutNode):
    class _BackgroundPropertiesHelper(LayoutNode):
        show: Expression | None = None
        transparency: Expression | None = None

    properties: _BackgroundPropertiesHelper = field(factory=_BackgroundPropertiesHelper)


class DataPointProperties(LayoutNode):
    class _DataPointPropertiesHelper(LayoutNode):
        fill: Expression | None = None

    properties: _DataPointPropertiesHelper = field(factory=_DataPointPropertiesHelper)
    selector: Selector | None = None


class GeneralProperties(LayoutNode):
    class _GeneralPropertiesHelper(LayoutNode):
        altText: Expression | None = None

    properties: _GeneralPropertiesHelper = field(factory=_GeneralPropertiesHelper)


class LabelsProperties(LayoutNode):
    class _LabelsPropertiesHelper(LayoutNode):
        background: Expression | None = None
        color: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        labelDisplayUnits: Expression | None = None
        labelStyle: Expression | None = None
        overflow: Expression | None = None
        percentageLabelPrecision: Expression | None = None
        position: Expression | None = None
        show: Expression | None = None

    properties: _LabelsPropertiesHelper = field(factory=_LabelsPropertiesHelper)


class LegendProperties(LayoutNode):
    class _LegendPropertiesHelper(LayoutNode):
        fontSize: Expression | None = None
        labelColor: Expression | None = None
        position: Expression | None = None
        show: Expression | None = None
        showTitle: Expression | None = None

    properties: _LegendPropertiesHelper = field(factory=_LegendPropertiesHelper)


class SlicesProperties(LayoutNode):
    class _SlicesPropertiesHelper(LayoutNode):
        innerRadiusRatio: Expression | None = None

    properties: _SlicesPropertiesHelper = field(factory=_SlicesPropertiesHelper)


class TitleProperties(LayoutNode):
    class _TitlePropertiesHelper(LayoutNode):
        alignment: Expression | None = None
        fontColor: Expression | None = None
        fontSize: Expression | None = None
        show: Expression | None = None
        text: Expression | None = None

    properties: _TitlePropertiesHelper = field(factory=_TitlePropertiesHelper)


class DonutChartProperties(LayoutNode):
    background: list[BackgroundProperties] = field(factory=lambda: [BackgroundProperties()])
    dataPoint: list[DataPointProperties] = field(factory=lambda: [DataPointProperties()])
    general: list[GeneralProperties] = field(factory=lambda: [GeneralProperties()])
    labels: list[LabelsProperties] = field(factory=lambda: [LabelsProperties()])
    legend: list[LegendProperties] = field(factory=lambda: [LegendProperties()])
    slices: list[SlicesProperties] = field(factory=lambda: [SlicesProperties()])
    title: list[TitleProperties] = field(factory=lambda: [TitleProperties()])


class DonutChart(BaseVisual):
    visualType: str = "donutChart"

    drillFilterOtherVisuals: bool = True
    objects: DonutChartProperties = field(factory=DonutChartProperties, repr=False)
