from typing import Annotated, Any, cast

from pydantic import Discriminator, Tag

from .aggregation import AggregationSource, DataSource
from .arithmetic import ArithmeticSource
from .base import Entity, SourceRef
from .column import ColumnSource
from .group import GroupSource
from .hierarchy import HierarchyLevelSource
from .literal import LiteralSource
from .measure import MeasureSource


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
        msg = f"Unknown Filter: {v.keys()}"
        raise ValueError(msg)
    return cast("str", v.__class__.__name__)


Source = Annotated[
    Annotated[HierarchyLevelSource, Tag("HierarchyLevelSource")]
    | Annotated[ColumnSource, Tag("ColumnSource")]
    | Annotated[GroupSource, Tag("GroupSource")]
    | Annotated[AggregationSource, Tag("AggregationSource")]
    | Annotated[MeasureSource, Tag("MeasureSource")]
    | Annotated[ArithmeticSource, Tag("ArithmeticSource")],
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
