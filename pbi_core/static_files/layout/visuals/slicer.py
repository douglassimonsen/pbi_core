# ruff: noqa: N815
from typing import Any

from pydantic import ConfigDict

from .base import BaseVisual


# TODO: remove Anys
class Slicer(BaseVisual):
    visualType: str = "slicer"
    model_config = ConfigDict(extra="forbid")
    columnProperties: Any = None
    syncGroup: Any = None
    display: Any = None
    cachedFilterDisplayItems: Any = None
    expansionStates: Any = None
