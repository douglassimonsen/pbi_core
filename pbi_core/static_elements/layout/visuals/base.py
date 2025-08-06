from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict

from ....lineage import LineageNode, LineageType
from .._base_node import LayoutNode
from ..filters import PrototypeQuery

if TYPE_CHECKING:
    pass


class BaseVisual(LayoutNode):
    model_config = ConfigDict(extra="allow")

    objects: Any = None
    prototypeQuery: PrototypeQuery
    projections: Any = None
    hasDefaultSort: bool = False
    drillFilterOtherVisuals: bool = False
    vcObjects: Any
    visualType: str = "unknown"

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        self.prototypeQuery.dependencies()
        return LineageNode(self, lineage_type)
