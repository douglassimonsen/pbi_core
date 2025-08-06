from typing import Annotated, Any, cast

from pydantic import BaseModel, Discriminator, Tag

from .aggregation import AggregationSource, DataSource
from .arithmetic import ArithmeticSource
from .base import Entity, SourceRef
from .column import ColumnSource
from .group import GroupSource
from .hierarchy import HierarchyLevelSource
from .literal import LiteralSource
from .measure import MeasureSource
from .proto import ProtoSourceRef


class RoleRef(BaseModel):
    Role: str


class TransformOutputRoleRef(BaseModel):
    TransformOutputRoleRef: RoleRef
    Name: str


def get_source(v: Any) -> str:  # noqa: PLR0911
    if isinstance(v, dict):
        if "Column" in v:
            return "ColumnSource"
        if "HierarchyLevel" in v:
            return "HierarchyLevelSource"
        if "GroupRef" in v:
            return "GroupSource"
        if "Aggregation" in v:
            return "AggregationSource"
        if "Measure" in v:
            return "MeasureSource"
        if "Arithmetic" in v:
            return "ArithmeticSource"
        if "SourceRef" in v:
            return "ProtoSourceRef"
        if "TransformOutputRoleRef" in v:
            return "TransformOutputRoleRef"
        msg = f"Unknown Filter: {v.keys()}"
        raise TypeError(msg)
    return cast("str", v.__class__.__name__)


Source = Annotated[
    Annotated[HierarchyLevelSource, Tag("HierarchyLevelSource")]
    | Annotated[ColumnSource, Tag("ColumnSource")]
    | Annotated[GroupSource, Tag("GroupSource")]
    | Annotated[AggregationSource, Tag("AggregationSource")]
    | Annotated[MeasureSource, Tag("MeasureSource")]
    | Annotated[ArithmeticSource, Tag("ArithmeticSource")]
    | Annotated[ProtoSourceRef, Tag("ProtoSourceRef")]
    | Annotated[TransformOutputRoleRef, Tag("TransformOutputRoleRef")],
    Discriminator(get_source),
]

__all__ = [
    "AggregationSource",
    "ArithmeticSource",
    "ColumnSource",
    "DataSource",
    "Entity",
    "GroupSource",
    "HierarchyLevelSource",
    "LiteralSource",
    "MeasureSource",
    "Source",
    "SourceRef",
]
