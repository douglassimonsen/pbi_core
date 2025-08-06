# ruff: noqa: N815


from pydantic import ConfigDict

from .._base_node import LayoutNode
from .base import BaseVisual
from .properties.base import Expression


class DataPointSelector(LayoutNode):
    metadata: str | None = None


class CategoryAxisProperties(LayoutNode):
    show: Expression | None = None
    preferredCategoryWidth: Expression | None = None


class CategoryAxis(LayoutNode):
    properties: CategoryAxisProperties
    selector: DataPointSelector | None = None


class DataPointProperties(LayoutNode):
    fill: Expression | None = None


# TODO: merge selector classes
class DataPoint(LayoutNode):
    properties: DataPointProperties
    selector: DataPointSelector | None = None


class LabelsProperties(LayoutNode):
    labelDisplayUnits: Expression | None = None
    labelOrientation: Expression | None = None
    labelPosition: Expression | None = None
    show: Expression | None = None


class Labels(LayoutNode):
    properties: LabelsProperties
    selector: DataPointSelector | None = None


class LegendProperties(LayoutNode):
    show: Expression | None = None


class Legend(LayoutNode):
    properties: LegendProperties
    selector: DataPointSelector | None = None


class ValueAxisProperties(LayoutNode):
    show: Expression | None = None


class ValueAxis(LayoutNode):
    properties: ValueAxisProperties
    selector: DataPointSelector | None = None


class ColumnChartColumnProperties(LayoutNode):
    categoryAxis: list[CategoryAxis]
    dataPoint: list[DataPoint]
    labels: list[Labels]
    legend: list[Legend]
    valueAxis: list[ValueAxis]


class ColumnChart(BaseVisual):
    visualType: str = "columnChart"
    model_config = ConfigDict(extra="forbid")

    objects: ColumnChartColumnProperties | None = None
