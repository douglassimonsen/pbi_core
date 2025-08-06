from enum import Enum
from typing import Any, Optional

from pydantic import Json

from ._base_node import LayoutNode
from .bookmark import LayoutBookmarkChild
from .filters import GlobalFilter
from .pod import Pod
from .resource_package import ResourcePackage
from .section import Section


class LayoutOptimization(Enum):
    DESKTOP = 0
    MOBILE = 1


class PublicCustomVisual(LayoutNode):
    pass  # TODO: find an example where this occurs


class LayoutConfig(LayoutNode):
    linguisticSchemaSyncVersion: Optional[int] = None
    defaultDrillFilterOtherVisuals: bool = True
    bookmarks: Optional[list[LayoutBookmarkChild]] = None
    activeSectionIndex: int
    themeCollection: Any
    slowDataSourceSettings: Optional[Any] = None
    settings: Optional[Any] = None
    version: float  # looks like a float
    objects: Optional[Any] = None
    filterSortOrder: Optional[int] = None  # TODO: to enum


class Layout(LayoutNode):
    id: int = -1
    reportId: int = -1
    filters: Json[list[GlobalFilter]] = []
    resourcePackages: list[ResourcePackage]
    sections: list[Section]
    config: Json[LayoutConfig]
    layoutOptimization: LayoutOptimization
    theme: Optional[str] = None
    pods: list[Pod] = []
    publicCustomVisuals: list[PublicCustomVisual] = []
    _xpath = []
