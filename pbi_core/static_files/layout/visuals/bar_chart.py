from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .column_property import ColumnProperty
from .properties.base import Expression


class LegendProperties(LayoutNode):
    class _LegendPropertiesHelper(LayoutNode):
        fontSize: Expression | None = None
        labelColor: Expression | None = None
        position: Expression | None = None
        show: Expression | None = None
        showTitle: Expression | None = None
        titleText: Expression | None = None

    properties: _LegendPropertiesHelper


class CategoryAxisProperties(LayoutNode):
    class _CategoryAxisPropertiesHelper(LayoutNode):
        axisType: Expression | None = None
        concatenateLabels: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        innerPadding: Expression | None = None
        labelColor: Expression | None = None
        maxMarginFactor: Expression | None = None
        position: Expression | None = None
        preferredCategoryWidth: Expression | None = None
        show: Expression | None = None
        showAxisTitle: Expression | None = None
        switchAxisPosition: Expression | None = None
        titleColor: Expression | None = None
        titleFontFamily: Expression | None = None
        titleFontSize: Expression | None = None

    properties: _CategoryAxisPropertiesHelper


class ValueAxisProperties(LayoutNode):
    class _ValueAxisPropertiesHelper(LayoutNode):
        axisScale: Expression | None = None
        fontSize: Expression | None = None
        gridlineColor: Expression | None = None
        gridlineShow: Expression | None = None
        invertAxis: Expression | None = None
        labelColor: Expression | None = None
        labelDisplayUnits: Expression | None = None
        show: Expression | None = None
        showAxisTitle: Expression | None = None
        titleFontFamily: Expression | None = None
        titleColor: Expression | None = None
        titleFontColor: Expression | None = None
        titleFontSize: Expression | None = None
        titleText: Expression | None = None

    properties: _ValueAxisPropertiesHelper


class LabelsProperties(LayoutNode):
    class _LabelsPropertiesHelper(LayoutNode):
        color: Expression | None = None
        enableBackground: Expression | None = None
        fontFamily: Expression | None = None
        fontSize: Expression | None = None
        labelDisplayUnits: Expression | None = None
        labelOverflow: Expression | None = None
        labelPosition: Expression | None = None
        labelPrecision: Expression | None = None
        show: Expression | None = None
        showAll: Expression | None = None

    properties: _LabelsPropertiesHelper
    selector: Selector | None = None


class DataPointProperties(LayoutNode):
    class _DataPointPropertiesHelper(LayoutNode):
        fill: Expression | None = None
        fillRule: Expression | None = None
        showAllDataPoints: Expression | None = None

    properties: _DataPointPropertiesHelper
    selector: Selector | None = None


class XAxisReferenceLineProperties(LayoutNode):
    class _XAxisReferenceLinePropertiesHelper(LayoutNode):
        displayName: Expression | None = None
        show: Expression | None = None
        value: Expression | None = None

    properties: _XAxisReferenceLinePropertiesHelper
    selector: Selector | None = None


class GeneralProperties(LayoutNode):
    class _GeneralPropertiesHelper(LayoutNode):
        responsive: Expression | None = None

    properties: _GeneralPropertiesHelper


class BarChartProperties(LayoutNode):
    categoryAxis: list[CategoryAxisProperties] | None = None
    dataPoint: list[DataPointProperties] | None = None
    general: list[GeneralProperties] | None = None
    labels: list[LabelsProperties] | None = None
    legend: list[LegendProperties] | None = None
    valueAxis: list[ValueAxisProperties] | None = None
    xAxisReferenceLine: list[XAxisReferenceLineProperties] | None = None


class BarChart(BaseVisual):
    visualType: str = "barChart"
    model_config = ConfigDict(extra="forbid")
    columnProperties: dict[str, ColumnProperty] | None = None
    objects: BarChartProperties | None = None
