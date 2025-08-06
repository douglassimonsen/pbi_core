# ruff: noqa: N815


from pydantic import ConfigDict

from .._base_node import LayoutNode
from ..selector import Selector
from .base import BaseVisual
from .column_property import ColumnProperty
from .properties.base import Expression


class DataBarsProperties(LayoutNode):
    axisColor: Expression
    hideText: Expression
    negativeColor: Expression
    positiveColor: Expression
    reverseDirection: Expression


class ColumnFormattingProperties(LayoutNode):
    dataBars: DataBarsProperties | None = None
    fontColor: Expression | None = None
    labelPrecision: Expression | None = None
    labelDisplayUnits: Expression | None = None


class ColumnFormatting(LayoutNode):
    properties: ColumnFormattingProperties
    selector: Selector | None = None


class TotalProperties(LayoutNode):
    totals: Expression


class Total(LayoutNode):
    properties: TotalProperties
    selector: Selector | None = None


class ValuesProperties(LayoutNode):
    backColor: Expression | None = None
    fontColor: Expression | None = None
    fontSize: Expression | None = None
    urlIcon: Expression | None = None
    backColorSecondary: Expression | None = None


class Values(LayoutNode):
    properties: ValuesProperties
    selector: Selector | None = None


class ColumnHeadersProperties(LayoutNode):
    autoSizeColumnWidth: Expression | None = None
    fontColor: Expression | None = None
    fontSize: Expression | None = None
    outline: Expression | None = None


class ColumnHeaders(LayoutNode):
    properties: ColumnHeadersProperties
    selector: Selector | None = None


class ColumnWidthProperties(LayoutNode):
    value: Expression


class ColumnWidth(LayoutNode):
    properties: ColumnWidthProperties
    selector: Selector | None = None


class GridProperties(LayoutNode):
    imageHeight: Expression | None = None
    textSize: Expression | None = None
    outlineColor: Expression | None = None
    rowPadding: Expression | None = None
    gridVertical: Expression | None = None


class Grid(LayoutNode):
    properties: GridProperties
    selector: Selector | None = None


class TableChartColumnProperties(LayoutNode):
    columnFormatting: list[ColumnFormatting] | None = None
    columnHeaders: list[ColumnHeaders] | None = None
    columnWidth: list[ColumnWidth] | None = None
    total: list[Total] | None = None
    values: list[Values] | None = None
    grid: list[Grid] | None = None


class TableChart(BaseVisual):
    visualType: str = "tableEx"
    objects: TableChartColumnProperties
    model_config = ConfigDict(extra="forbid")
    columnProperties: dict[str, ColumnProperty] | None = None
