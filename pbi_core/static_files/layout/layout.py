# ruff: noqa: N815
from enum import Enum
from typing import Annotated, Any, cast

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
    customTheme: ThemeInfo | None = None


class SettingsV2(LayoutNode):
    useNewFilterPaneExperience: bool
    allowChangeFilterTypes: bool
    useStylableVisualContainerHeader: bool
    useEnhancedTooltips: bool = True
    exportDataMode: int  # def an enum
    allowDataPointLassoSelect: bool = False


class SettingsV1(LayoutNode):
    isPersistentUserStateDisabled: bool
    hideVisualContainerHeader: bool
    useStylableVisualContainerHeader: bool = True


def get_settings(v: Any) -> str:
    if isinstance(v, dict):
        if "isPersistentUserStateDisabled" in v:
            return "SettingsV1"
        if "useNewFilterPaneExperience" in v:
            return "SettingsV2"
        msg = f"Unknown Filter: {v.keys()}"
        raise ValueError(msg)
    return cast("str", v.__class__.__name__)


Settings = Annotated[
    Annotated[SettingsV1, Tag("SettingsV1")] | Annotated[SettingsV2, Tag("SettingsV2")],
    Discriminator(get_settings),
]


class LayoutConfig(LayoutNode):
    linguisticSchemaSyncVersion: int | None = None
    defaultDrillFilterOtherVisuals: bool = True
    bookmarks: list[LayoutBookmarkChild] | None = None
    activeSectionIndex: int
    themeCollection: ThemeCollection
    slowDataSourceSettings: Any | None = None
    settings: Settings | None = None
    version: float  # looks like a float
    objects: Any | None = None
    filterSortOrder: int | None = None  # TODO: to enum


class Layout(LayoutNode):
    id: int = -1
    reportId: int = -1
    filters: Json[list[GlobalFilter]] = []
    resourcePackages: list[ResourcePackage]
    sections: list[Section]
    config: Json[LayoutConfig]
    layoutOptimization: LayoutOptimization
    theme: str | None = None
    pods: list[Pod] = []
    publicCustomVisuals: list[PublicCustomVisual] = []
    _xpath = []
