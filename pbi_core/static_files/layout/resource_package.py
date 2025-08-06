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
    _parent: "ResourcePackageDetails"
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
    _parent: "ResourcePackage"
    disabled: bool
    items: list[ResourcePackageItem] = []
    type: ResourcePackageDetailsType
    name: str
    id: Optional[int] = None


class ResourcePackage(LayoutNode):
    _parent: "Layout"
    resourcePackage: ResourcePackageDetails
