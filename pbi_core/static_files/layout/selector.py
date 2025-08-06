from enum import StrEnum

from ._base_node import LayoutNode
from .condition import ComparisonCondition


class PropertyDefSelectorId(StrEnum):
    default = "default"
    hover = "hover"
    id = "id"
    selected = "selected"


class DataViewWildcard(LayoutNode):
    matchingOption: int
    roles: list[str] | None = None


class SelectorData(LayoutNode):
    roles: list[str] | None = None
    dataViewWildcard: DataViewWildcard | None = None
    scopeId: ComparisonCondition | None = None


# TODO: possibly replace with a union?
class Selector(LayoutNode):
    id: PropertyDefSelectorId | None = None
    metadata: str | None = None
    data: list[SelectorData] | None = None
