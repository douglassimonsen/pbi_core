# ruff: noqa: N815


from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.selector import Selector

from .base import BaseVisual
from .column_property import ColumnProperty
from .properties.base import Expression


class CategoryAxisProperties(LayoutNode):
    show: Expression | None = None
    preferredCategoryWidth: Expression | None = None
    concatenateLabels: Expression | None = None
    maxMarginFactor: Expression | None = None
    innerPadding: Expression | None = None
    fontSize: Expression | None = None
    titleFontSize: Expression | None = None
    showAxisTitle: Expression | None = None
    titleColor: Expression | None = None


class CategoryAxis(LayoutNode):
    properties: CategoryAxisProperties
    selector: Selector | None = None


class DataPointProperties(LayoutNode):
    fill: Expression | None = None
    fillRule: Expression | None = None


class DataPoint(LayoutNode):
    properties: DataPointProperties
    selector: Selector | None = None


class LabelsProperties(LayoutNode):
    fontSize: Expression | None = None
    labelDisplayUnits: Expression | None = None
    labelOrientation: Expression | None = None
    labelPosition: Expression | None = None
    show: Expression | None = None


class Labels(LayoutNode):
    properties: LabelsProperties
    selector: Selector | None = None


class LegendProperties(LayoutNode):
    show: Expression | None = None
    labelColor: Expression | None = None
    showTitle: Expression | None = None
    fontSize: Expression | None = None
    position: Expression | None = None


class Legend(LayoutNode):
    properties: LegendProperties
    selector: Selector | None = None


class ValueAxisProperties(LayoutNode):
    show: Expression | None = None
    gridlineShow: Expression | None = None
    titleFontFamily: Expression | None = None
    fontSize: Expression | None = None


class ValueAxis(LayoutNode):
    properties: ValueAxisProperties
    selector: Selector | None = None


class ColumnChartColumnProperties(LayoutNode):
    categoryAxis: list[CategoryAxis] | None = None
    dataPoint: list[DataPoint] | None = None
    labels: list[Labels] | None = None
    legend: list[Legend] | None = None
    valueAxis: list[ValueAxis] | None = None


class ColumnChart(BaseVisual):
    visualType: str = "columnChart"
    model_config = ConfigDict(extra="forbid")

    objects: ColumnChartColumnProperties | None = None
    columnProperties: dict[str, ColumnProperty] | None = None
