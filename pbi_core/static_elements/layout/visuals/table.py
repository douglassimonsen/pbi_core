from pydantic import ConfigDict

from .base import BaseVisual


class TableChart(BaseVisual):
    visualType: str = "tableEx"
    model_config = ConfigDict(extra="forbid")
