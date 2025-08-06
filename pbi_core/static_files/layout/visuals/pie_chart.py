# ruff: noqa: N815
from typing import Any

from pydantic import ConfigDict

from .base import BaseVisual


# TODO: remove Anys
class PieChart(BaseVisual):
    visualType: str = "pieChart"
    model_config = ConfigDict(extra="forbid")
    columnProperties: Any = None
