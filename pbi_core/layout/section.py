from enum import IntEnum
from typing import Any, Optional
from uuid import UUID

from pydantic import ConfigDict, Json

from ._base_node import LayoutNode


class DisplayOption(IntEnum):
    FIT_TO_PAGE = 0
    FIT_TO_WIDTH = 1
    ACTUAL_SIZE = 2
    MOBILE = 3


class SectionConfig(LayoutNode):
    model_config = ConfigDict(extra="allow")


class Section(LayoutNode):
    height: int
    width: int
    displayOption: DisplayOption
    config: Json[SectionConfig]
    objectId: Optional[UUID] = None
    visualContainers: list[Any]
    ordinal: int
    filters: Json[Any]
    displayName: str
    name: str
    id: Optional[int] = None
