# ruff: noqa: N815

from pydantic import ConfigDict

from .base import BaseVisual
from .column_property import ColumnProperty


class BarChart(BaseVisual):
    visualType: str = "barChart"
    model_config = ConfigDict(extra="forbid")
    columnProperties: dict[str, ColumnProperty] = None
