# ruff: noqa: N815

from pydantic import ConfigDict

from .base import BaseVisual


class BarChart(BaseVisual):
    visualType: str = "barChart"
    model_config = ConfigDict(extra="forbid")
    columnProperties: int = None
