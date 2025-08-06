from pydantic import ConfigDict

from .base import BaseVisual


class PieChart(BaseVisual):
    visualType: str = "pieChart"
    model_config = ConfigDict(extra="forbid")
