# ruff: noqa: N815
from enum import IntEnum
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import ConfigDict, Json

from pbi_core.static_files.model_references import ModelColumnReference, ModelMeasureReference

from ._base_node import LayoutNode
from .filters import PageFilter
from .visual_container import VisualContainer

if TYPE_CHECKING:
    from .layout import Layout


class DisplayOption(IntEnum):
    FIT_TO_PAGE = 0
    FIT_TO_WIDTH = 1
    ACTUAL_SIZE = 2
    MOBILE = 3


class SectionConfig(LayoutNode):
    model_config = ConfigDict(extra="allow")


class Section(LayoutNode):
    _parent: "Layout"  # pyright: ignore reportIncompatibleVariableOverride=false
    height: int
    width: int
    displayOption: DisplayOption
    config: Json[SectionConfig]
    objectId: UUID | None = None
    visualContainers: list[VisualContainer]
    ordinal: int = 0
    filters: Json[list[PageFilter]]
    displayName: str
    name: str
    id: int | None = None

    def get_ssas_elements(
        self,
        *,
        include_visuals: bool = True,
        include_filters: bool = True,
    ) -> set[ModelColumnReference | ModelMeasureReference]:
        """Returns the SSAS elements (columns and measures) this report page is directly dependent on."""
        ret: set[ModelColumnReference | ModelMeasureReference] = set()
        if include_visuals:
            for viz in self.visualContainers:
                ret.update(viz.get_ssas_elements())
        if include_filters:
            for f in self.filters:
                ret.update(f.get_ssas_elements())
        return ret
