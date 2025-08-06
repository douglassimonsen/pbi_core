from typing import Any, Optional

from pydantic import Json

from ._base_node import LayoutNode
from .resource_package import ResourcePackage
from .section import Section


class Layout(LayoutNode):
    id: int = -1
    reportId: int = -1
    filters: Json[Any]
    resourcePackages: list[ResourcePackage]
    sections: list[Section]
    config: Json[Any]
    layoutOptimization: Any
    theme: Optional[str] = None
    pods: list[Any] = []
    publicCustomVisuals: list[Any] = []
