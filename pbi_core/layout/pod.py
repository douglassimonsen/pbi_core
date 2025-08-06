import inspect
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

from pydantic import Json

from ._base_node import LayoutNode
from .sources import ColumnSource

if TYPE_CHECKING:
    from .layout import Layout


class Parameter(LayoutNode):
    parent: "Pod"

    name: str
    boundFilter: str
    fieldExpr: Optional[ColumnSource] = None
    isLegacySingleSelection: Optional[bool] = False
    asAggregation: Optional[bool] = False


class PodType(IntEnum):
    NA1 = 1
    NA2 = 2


class Pod(LayoutNode):
    parent: "Layout"

    id: Optional[int] = None
    name: str
    boundSection: str
    config: Json[Any]
    parameters: Json[list[Parameter]] = []
    type: Optional[PodType] = None
    referenceScope: Optional[int] = None
    cortanaEnabled: Optional[bool] = None
    objectId: Optional[UUID] = None


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
