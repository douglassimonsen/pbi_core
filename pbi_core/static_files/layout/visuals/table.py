# ruff: noqa: N815


from pydantic import ConfigDict

from .._base_node import LayoutNode
from .base import BaseVisual
from .properties.base import Expression


class DataBarsProperties(LayoutNode):
    axisColor: Expression
    hideText: Expression
    negativeColor: Expression
    positiveColor: Expression
    reverseDirection: Expression


class ColumnFormattingProperties(LayoutNode):
    dataBars: DataBarsProperties | None = None
    labelPrecision: Expression | None = None
    labelDisplayUnits: Expression | None = None


class MatchingOption(LayoutNode):
    matchingOption: int


class DataViewWildcard(LayoutNode):
    dataViewWildcard: MatchingOption | None = None
    roles: list[str] | None = None


class ColumnFormattingSelector(LayoutNode):
    metadata: str | None = None
    data: list[DataViewWildcard] | None = None


class ColumnFormatting(LayoutNode):
    properties: ColumnFormattingProperties
    selector: ColumnFormattingSelector | None = None


class TotalProperties(LayoutNode):
    totals: Expression


class Total(LayoutNode):
    properties: TotalProperties
    selector: ColumnFormattingSelector | None = None


class ValuesProperties(LayoutNode):
    backColor: Expression | None = None
    fontColor: Expression | None = None
    fontSize: Expression | None = None
    urlIcon: Expression | None = None


class Values(LayoutNode):
    properties: ValuesProperties
    selector: ColumnFormattingSelector | None = None


class ColumnHeadersProperties(LayoutNode):
    fontColor: Expression | None = None
    fontSize: Expression | None = None
    outline: Expression | None = None


class ColumnHeaders(LayoutNode):
    properties: ColumnHeadersProperties
    selector: ColumnFormattingSelector | None = None


class ColumnWidthProperties(LayoutNode):
    value: Expression


class ColumnWidth(LayoutNode):
    properties: ColumnWidthProperties
    selector: ColumnFormattingSelector | None = None


class GridProperties(LayoutNode):
    imageHeight: Expression | None = None
    textSize: Expression | None = None


class Grid(LayoutNode):
    properties: GridProperties
    selector: ColumnFormattingSelector | None = None


class TableChartColumnProperties(LayoutNode):
    columnFormatting: list[ColumnFormatting] | None = None
    columnHeaders: list[ColumnHeaders] | None = None
    columnWidth: list[ColumnWidth] | None = None
    total: list[Total] | None = None
    values: list[Values] | None = None
    grid: list[Grid] | None = None


class ColumnProperty(LayoutNode):
    displayName: str


class TableChart(BaseVisual):
    visualType: str = "tableEx"
    objects: TableChartColumnProperties
    model_config = ConfigDict(extra="forbid")
    columnProperties: dict[str, ColumnProperty] | None = None
