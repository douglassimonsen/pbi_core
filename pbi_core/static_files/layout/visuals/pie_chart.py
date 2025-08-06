# ruff: noqa: N815

from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode

from .base import BaseVisual


class PieChartColumnProperties(LayoutNode):
    pass


class PieChart(BaseVisual):
    visualType: str = "pieChart"
    model_config = ConfigDict(extra="forbid")
    columnProperties: PieChartColumnProperties | None = None
