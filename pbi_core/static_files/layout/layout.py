# ruff: noqa: N815
from enum import Enum
from typing import Any

from pydantic import Json

from pbi_core.static_files.model_references import ModelColumnReference, ModelMeasureReference

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
    baseTheme: ThemeInfo | None = None
    customTheme: ThemeInfo | None = None


class Settings(LayoutNode):
    allowChangeFilterTypes: bool = True
    allowDataPointLassoSelect: bool = False
    exportDataMode: int = 0  # def an enum
    hideVisualContainerHeader: bool = False
    isPersistentUserStateDisabled: bool = False
    useEnhancedTooltips: bool = True
    useNewFilterPaneExperience: bool = True
    useStylableVisualContainerHeader: bool = True
    useCrossReportDrillthrough: bool = False
    defaultFilterActionIsDataFilter: bool = False
    disableFilterPaneSearch: bool = False
    allowInlineExploration: bool = True
    optOutNewFilterPaneExperience: bool = False
    enableDeveloperMode: bool = False
    filterPaneHiddenInEditMode: bool = False
    queryLimitOption: int = 6
    useDefaultAggregateDisplayName: bool = True


# TODO: remove Anys
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

    def get_ssas_elements(
        self,
        *,
        include_sections: bool = True,
        include_filters: bool = True,
    ) -> set[ModelColumnReference | ModelMeasureReference]:
        """Returns the SSAS elements (columns and measures) this report is directly dependent on."""
        ret: set[ModelColumnReference | ModelMeasureReference] = set()
        if include_filters:
            for f in self.filters:
                ret.update(f.get_ssas_elements())
        if include_sections:
            for s in self.sections:
                ret.update(s.get_ssas_elements())
        return ret
