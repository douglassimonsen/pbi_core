# ruff: noqa: N815

from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode

from .base import BaseVisual
from .table import ColumnProperty


class SyncGroup(LayoutNode):
    groupName: str
    fieldChanges: bool


class Display(LayoutNode):
    mode: str


class Slicer(BaseVisual):
    visualType: str = "slicer"
    model_config = ConfigDict(extra="forbid")
    columnProperties: dict[str, ColumnProperty] | None = None
    syncGroup: SyncGroup | None = None
    display: Display | None = None
    cachedFilterDisplayItems: int | None = None
    expansionStates: int | None = None
