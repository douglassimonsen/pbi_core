from typing import Any

from pydantic import ConfigDict

from .._base_node import LayoutNode


class TextBox(LayoutNode):
    visualType: str = "textbox"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: Any
    vcObjects: Any = None
    display: Any = None
