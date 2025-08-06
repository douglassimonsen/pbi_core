from pydantic import ConfigDict

from .base import BaseVisual


class ColumnChart(BaseVisual):
    visualType: str = "columnChart"
    model_config = ConfigDict(extra="forbid")
