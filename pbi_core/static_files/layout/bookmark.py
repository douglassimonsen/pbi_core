# ruff: noqa: N815
from enum import Enum
from typing import TYPE_CHECKING, Annotated, Any, cast

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
    metadata: list[str] | None = None


class Highlight(LayoutNode):
    selection: list[HighlightSelection]
    filterExpressionMetadata: Any | None = None


class DisplayMode(Enum):
    hidden = "hidden"


class Display(LayoutNode):
    mode: DisplayMode


class BookmarkPartialVisual(LayoutNode):
    visualType: str
    objects: dict[str, Any]
    orderBy: list[Any] | None = None
    activeProjections: dict[str, list[Source]] | None = None
    display: Display | None = None
    expansionStates: Any | None = None


class BookmarkVisual(LayoutNode):
    filters: BookmarkFilters | None = None
    singleVisual: BookmarkPartialVisual
    highlight: Highlight | None = None


class BookmarkSection(LayoutNode):
    _parent: "ExplorationState"  # pyright: ignore reportIncompatibleVariableOverride=false

    visualContainers: dict[str, BookmarkVisual] | None = None
    filters: BookmarkFilters | None = None
    visualContainerGroups: Any | None = None


class ExplorationState(LayoutNode):
    _parent: "Bookmark"  # pyright: ignore reportIncompatibleVariableOverride=false

    version: float
    sections: dict[str, BookmarkSection]
    activeSection: str  # matches the section name?
    filters: BookmarkFilters | None = None
    objects: Any | None = None


class BookmarkOptions(LayoutNode):
    _parent: "Bookmark"  # pyright: ignore reportIncompatibleVariableOverride=false

    targetVisualNames: list[str] | None = None
    applyOnlyToTargetVisuals: bool = False
    suppressActiveSection: bool = False
    suppressData: bool = False
    suppressDisplay: bool = False


class Bookmark(LayoutNode):
    _parent: "Layout"  # pyright: ignore reportIncompatibleVariableOverride=false

    options: BookmarkOptions | None
    explorationState: ExplorationState | None
    name: str  # acts as an ID
    displayName: str

    def match_current_filters(self) -> None:
        raise NotImplementedError

    @staticmethod
    def new(  # noqa: PLR0913
        section: "Section",
        selected_visuals: list["BaseVisual"],
        bookmark_name: str,
        *,
        include_data: bool = True,
        include_display: bool = True,
        include_current_page: bool = True,
    ) -> "Bookmark":
        raise NotImplementedError


class BookmarkFolder(LayoutNode):
    _parent: "Layout"  # pyright: ignore reportIncompatibleVariableOverride=false
    displayName: str
    name: str  # acts as an ID
    children: list[Bookmark]


def get_bookmark_type(v: Any) -> str:
    if isinstance(v, dict):
        if "explorationState" in v:
            return "Bookmark"
        return "BookmarkFolder"
    return cast("str", v.__class__.__name__)


LayoutBookmarkChild = Annotated[
    Annotated[Bookmark, Tag("Bookmark")] | Annotated[BookmarkFolder, Tag("BookmarkFolder")],
    Discriminator(get_bookmark_type),
]
