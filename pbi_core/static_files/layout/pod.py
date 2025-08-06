from enum import IntEnum
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

from pydantic import Json

from ._base_node import LayoutNode
from .sources import ColumnSource

if TYPE_CHECKING:
    from .layout import Layout


class Parameter(LayoutNode):
    _parent: "Pod"

    name: str
    boundFilter: str
    fieldExpr: Optional[ColumnSource] = None
    isLegacySingleSelection: Optional[bool] = False
    asAggregation: Optional[bool] = False


class PodType(IntEnum):
    NA1 = 1
    NA2 = 2


class Pod(LayoutNode):
    _parent: "Layout"

    id: Optional[int] = None
    name: str
    boundSection: str
    config: Json[Any]
    parameters: Json[list[Parameter]] = []
    type: Optional[PodType] = None
    referenceScope: Optional[int] = None
    cortanaEnabled: Optional[bool] = None
    objectId: Optional[UUID] = None
