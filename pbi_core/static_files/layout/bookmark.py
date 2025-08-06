from enum import Enum
from typing import TYPE_CHECKING, Annotated, Any, Optional, Union, cast

from pydantic import Discriminator, Tag

from ._base_node import LayoutNode
from .condition import BasicConditions
from .filters import BookmarkFilter
from .sources import Source

if TYPE_CHECKING:
    from .layout import Layout
    from .section import Section
    from .visuals.base import BaseVisual


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
    activeProjections: Optional[dict[str, list[Source]]] = None
    display: Optional[Display] = None
    expansionStates: Optional[Any] = None


class BookmarkVisual(LayoutNode):
    filters: Optional[BookmarkFilters] = None
    singleVisual: BookmarkPartialVisual
    highlight: Optional[Highlight] = None


class BookmarkSection(LayoutNode):
    _parent: "ExplorationState"

    visualContainers: Optional[dict[str, BookmarkVisual]] = None
    filters: Optional[BookmarkFilters] = None
    visualContainerGroups: Optional[Any] = None


class ExplorationState(LayoutNode):
    _parent: "Bookmark"

    version: float
    sections: dict[str, BookmarkSection]
    activeSection: str  # matches the section name?
    filters: Optional[BookmarkFilters] = None
    objects: Optional[Any] = None


class BookmarkOptions(LayoutNode):
    _parent: "Bookmark"

    targetVisualNames: Optional[list[str]] = None
    applyOnlyToTargetVisuals: bool = False
    suppressActiveSection: bool = False
    suppressData: bool = False
    suppressDisplay: bool = False


class Bookmark(LayoutNode):
    _parent: "Layout"

    options: Optional[BookmarkOptions]
    explorationState: Optional[ExplorationState]
    name: str  # acts as an ID
    displayName: str

    def match_current_filters(self) -> None:
        raise NotImplementedError
    
    @staticmethod
    def new(section: "Section", selected_visuals: list["BaseVisual"], bookmark_name: str, include_data: bool=True, include_display: bool=True, include_current_page: bool=True):
        raise NotImplementedError


class BookmarkFolder(LayoutNode):
    _parent: "Layout"
    displayName: str
    name: str  # acts as an ID
    children: list[Bookmark]


def get_bookmark_type(v: Any) -> str:
    if isinstance(v, dict):
        if "explorationState" in v.keys():
            return "Bookmark"
        return "BookmarkFolder"
    else:
        return cast(str, v.__class__.__name__)


LayoutBookmarkChild = Annotated[
    Union[
        Annotated[Bookmark, Tag("Bookmark")],
        Annotated[BookmarkFolder, Tag("BookmarkFolder")],
    ],
    Discriminator(get_bookmark_type),
]
