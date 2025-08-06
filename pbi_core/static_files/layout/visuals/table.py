# ruff: noqa: N815
from typing import Any

from pydantic import ConfigDict

from .base import BaseVisual


# TODO: remove Anys
class TableChart(BaseVisual):
    visualType: str = "tableEx"
    columnProperties: Any = None
    model_config = ConfigDict(extra="forbid")
