from enum import Enum
from typing import Annotated, Any, Optional, Union, cast

from pydantic import Discriminator, Json, Tag

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


class ThemeInfo(LayoutNode):
    name: str
    version: float
    type: int  # def an enum


class ThemeCollection(LayoutNode):
    baseTheme: ThemeInfo
    customTheme: Optional[ThemeInfo] = None


class SettingsV2(LayoutNode):
    useNewFilterPaneExperience: bool
    allowChangeFilterTypes: bool
    useStylableVisualContainerHeader: bool
    exportDataMode: int  # def an enum


class SettingsV1(LayoutNode):
    isPersistentUserStateDisabled: bool
    hideVisualContainerHeader: bool
    useStylableVisualContainerHeader: bool = True


def get_settings(v: Any) -> str:
    if isinstance(v, dict):
        if "isPersistentUserStateDisabled" in v.keys():
            return "SettingsV1"
        elif "useNewFilterPaneExperience" in v.keys():
            return "SettingsV2"
        else:
            raise ValueError(f"Unknown Filter: {v.keys()}")
    else:
        return cast(str, v.__class__.__name__)


Settings = Annotated[
    Union[
        Annotated[SettingsV1, Tag("SettingsV1")],
        Annotated[SettingsV2, Tag("SettingsV2")],
    ],
    Discriminator(get_settings),
]


class LayoutConfig(LayoutNode):
    linguisticSchemaSyncVersion: Optional[int] = None
    defaultDrillFilterOtherVisuals: bool = True
    bookmarks: Optional[list[LayoutBookmarkChild]] = None
    activeSectionIndex: int
    themeCollection: ThemeCollection
    slowDataSourceSettings: Optional[Any] = None
    settings: Optional[Settings] = None
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
