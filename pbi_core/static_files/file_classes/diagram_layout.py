from typing import Optional
from uuid import UUID

from pydantic_extra_types.semantic_version import SemanticVersion

from ._base import BaseFileModel

base_val = bool | int | str


class Position(BaseFileModel):
    x: int | float
    y: int | float


class Size(BaseFileModel):
    height: int | float
    width: int | float


class Node(BaseFileModel):
    location: Position
    nodeIndex: str
    nodeLineageTag: Optional[UUID] = None
    size: Size
    zIndex: int


class Diagram(BaseFileModel):
    ordinal: int
    scrollPosition: Position
    nodes: list[Node]
    name: str
    zoomValue: int
    pinKeyFieldsToTop: bool
    showExtraHeaderInfo: bool
    hideKeyFieldsWhenCollapsed: bool
    tablesLocked: bool = False


class DiagramLayout(BaseFileModel):
    version: SemanticVersion
    diagrams: list[Diagram]
    selectedDiagram: str
    defaultDiagram: str
