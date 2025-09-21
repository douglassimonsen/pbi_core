from enum import IntEnum
from uuid import UUID

from pydantic import Json

from pbi_core.pydantic.attrs import define

from ._base_node import LayoutNode
from .sources import ColumnSource


@define()
class Parameter(LayoutNode):
    name: str
    boundFilter: str
    fieldExpr: ColumnSource | None = None
    isLegacySingleSelection: bool | None = False
    asAggregation: bool | None = False


class PodType(IntEnum):
    NA1 = 1
    NA2 = 2


@define()
class PodConfig(LayoutNode):
    acceptsFilterContext: bool = False


@define()
class Pod(LayoutNode):
    id: int | None = None
    name: str
    boundSection: str
    config: Json[PodConfig]
    parameters: Json[list[Parameter]] = []
    type: PodType | None = None
    referenceScope: int | None = None
    cortanaEnabled: bool | None = None
    objectId: UUID | None = None
