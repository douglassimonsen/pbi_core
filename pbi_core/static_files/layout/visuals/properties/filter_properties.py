from pbi_core.static_files.layout._base_node import LayoutNode

from .base import Expression


class FilterProperties(LayoutNode):
    isInvertedSelectionMode: Expression  # noqa: N815


class FilterPropertiesContainer(LayoutNode):
    properties: FilterProperties


class FilterObjects(LayoutNode):
    general: list[FilterPropertiesContainer] | None = None
