# ruff: noqa: N815

from pydantic import ConfigDict

from .base import BaseVisual
from .column_property import ColumnProperty


class PieChart(BaseVisual):
    visualType: str = "pieChart"
    model_config = ConfigDict(extra="forbid")
    columnProperties: dict[str, ColumnProperty] | None = None
