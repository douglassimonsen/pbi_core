import inspect
from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from ._base_node import LayoutNode

if TYPE_CHECKING:
    from .layout import Layout


class ResourcePackageItemType(IntEnum):
    JS = 0
    CSS = 1
    PNG = 3
    PBIVIZ = 5
    NA = 100
    TOPO = 200
    JSON2 = 201
    JSON = 202


class ResourcePackageItem(LayoutNode):
    parent: "ResourcePackageDetails"
    name: Optional[str] = None
    path: str
    type: ResourcePackageItemType
    resourcePackageId: Optional[int] = None
    resourcePackageItemBlobInfoId: Optional[int] = None
    id: Optional[int] = None


class ResourcePackageDetailsType(IntEnum):
    JS = 0
    CUSTOM_THEME = 1
    BASE_THEME = 2


class ResourcePackageDetails(LayoutNode):
    parent: "ResourcePackage"
    disabled: bool
    items: list[ResourcePackageItem] = []
    type: ResourcePackageDetailsType
    name: str
    id: Optional[int] = None


class ResourcePackage(LayoutNode):
    parent: "Layout"
    resourcePackage: ResourcePackageDetails


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
