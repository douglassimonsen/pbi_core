import inspect
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

from ._base_node import LayoutNode
from .condition import BasicConditions
from .filters import BookmarkFilter
from .sources import VisualFilterSource

if TYPE_CHECKING:
    from .layout import Layout


class BookmarkFilters(LayoutNode):
    byExpr: list[BookmarkFilter] = []
    byType: list[BookmarkFilter] = []
    byName: dict[str, BookmarkFilter] = {}


class HighlightScope(LayoutNode):
    scopeId: BasicConditions


class HighlightSelection(LayoutNode):
    dataMap: dict[str, list[HighlightScope]]
    metadata: Optional[list[str]] = None


class Highlight(LayoutNode):
    selection: list[HighlightSelection]
    filterExpressionMetadata: Optional[Any] = None


class DisplayMode(Enum):
    hidden = "hidden"


class Display(LayoutNode):
    mode: DisplayMode


class BookmarkPartialVisual(LayoutNode):
    visualType: str
    objects: dict[str, Any]
    orderBy: Optional[list[Any]] = None
    activeProjections: Optional[dict[str, list[VisualFilterSource]]] = None
    display: Optional[Display] = None
    expansionStates: Optional[Any] = None


class BookmarkVisualContainer(LayoutNode):
    filters: Optional[BookmarkFilters] = None
    singleVisual: BookmarkPartialVisual
    highlight: Optional[Highlight] = None


class BookmarkVisual(LayoutNode):
    filters: Optional[BookmarkFilters] = None
    singleVisual: BookmarkPartialVisual
    highlight: Optional[Highlight] = None


class BookmarkSection(LayoutNode):
    parent: "ExplorationState"

    visualContainers: Optional[dict[str, BookmarkVisual]] = None
    filters: Optional[BookmarkFilters] = None
    visualContainerGroups: Optional[Any] = None


class ExplorationState(LayoutNode):
    parent: "Bookmark"

    version: float
    sections: dict[str, BookmarkSection]
    activeSection: str  # matches the section name?
    filters: Optional[BookmarkFilters] = None
    objects: Optional[Any] = None


class BookmarkOptions(LayoutNode):
    parent: "Bookmark"

    targetVisualNames: Optional[list[str]] = None
    applyOnlyToTargetVisuals: bool = False
    suppressActiveSection: bool = False
    suppressData: bool = False
    suppressDisplay: bool = False


class Bookmark(LayoutNode):
    parent: "Layout"

    options: Optional[BookmarkOptions] = None
    explorationState: Optional[ExplorationState] = None
    name: str  # acts as an ID
    displayName: str
    children: Optional[Any] = None

    def match_current_filters(self) -> None:
        raise NotImplementedError


class BookmarkFolder(LayoutNode):
    parent: "Layout"
    displayName: str
    name: str  # acts as an ID
    children: list[Bookmark]
    options: Optional[dict[str, Any]] = None


"""
woo boy. Why is this code here? Well, we want a parent attribute on the objects to make user navigation easier
This has to be a non-private attribute due to a bug in pydantic right now.
We know we'll add the parent attribute after pydantic does it's work, but we want mypy to think the parent is
always there. Therefore we check all objects with parents and make the default None so the "is_required" becomes False
https://github.com/pydantic/pydantic/blob/a764871df98c8932e9b7bc10d861053d110a99e4/pydantic/fields.py#L572
"""
for name, obj in list(globals().items()):
    if inspect.isclass(obj) and issubclass(obj, LayoutNode) and "parent" in obj.model_fields:
        obj.model_fields["parent"].default = None
