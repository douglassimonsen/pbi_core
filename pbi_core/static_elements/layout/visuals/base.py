from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict

from .._base_node import LayoutNode

if TYPE_CHECKING:
    pass


class BaseVisual(LayoutNode):
    model_config = ConfigDict(extra="allow")

    objects: Any = None
    prototypeQuery: Any = None
    projections: Any = None
    hasDefaultSort: bool = False
    drillFilterOtherVisuals: bool = False
    vcObjects: Any
    visualType: str = "unknown"
