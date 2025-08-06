import inspect
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

from pydantic import ConfigDict, Json

from ._base_node import LayoutNode

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
    parent: "Layout"
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
