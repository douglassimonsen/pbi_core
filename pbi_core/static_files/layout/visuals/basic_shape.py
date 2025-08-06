from typing import Any

from pydantic import ConfigDict

from .._base_node import LayoutNode


class BasicShape(LayoutNode):
    visualType: str = "basicShape"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: Any
    vcObjects: Any = None
