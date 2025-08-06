from pydantic import ConfigDict

from .base import BaseVisual


class Slicer(BaseVisual):
    visualType: str = "slicer"
    model_config = ConfigDict(extra="forbid")
