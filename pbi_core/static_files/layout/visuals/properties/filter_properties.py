
from ..._base_node import LayoutNode
from .base import Expression


class FilterProperties(LayoutNode):
    isInvertedSelectionMode: Expression


class FilterPropertiesContainer(LayoutNode):
    properties: FilterProperties


class FilterObjects(LayoutNode):
    general: list[FilterPropertiesContainer] | None = None
