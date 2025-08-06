from typing import Annotated, Any, Union

from pydantic import Discriminator, Tag

from .aggregation import AggregationSource, DataSource
from .arithmetic import ArithmeticSource
from .base import Entity, SourceRef
from .column import ColumnSource
from .group import GroupSource
from .hierarchy import HierarchyLevelSource
from .literal import LiteralSource
from .measure import MeasureSource


def get_source(v: Any) -> str:
    if isinstance(v, dict):
        if "Column" in v.keys():
            return "ColumnSource"
        elif "HierarchyLevel" in v.keys():
            return "HierarchyLevelSource"
        elif "GroupRef" in v.keys():
            return "GroupSource"
        elif "Aggregation" in v.keys():
            return "AggregationSource"
        elif "Measure" in v.keys():
            return "MeasureSource"
        elif "Arithmetic" in v.keys():
            return "ArithmeticSource"
        else:
            raise ValueError(f"Unknown Filter: {v.keys()}")
    else:
        return v.__class__.__name__


Source = Annotated[
    Union[
        Annotated[HierarchyLevelSource, Tag("HierarchyLevelSource")],
        Annotated[ColumnSource, Tag("ColumnSource")],
        Annotated[GroupSource, Tag("GroupSource")],
        Annotated[AggregationSource, Tag("AggregationSource")],
        Annotated[MeasureSource, Tag("MeasureSource")],
        Annotated[ArithmeticSource, Tag("ArithmeticSource")],
    ],
    Discriminator(get_source),
]

__all__ = [
    "AggregationSource",
    "DataSource",
    "ArithmeticSource",
    "Entity",
    "SourceRef",
    "ColumnSource",
    "GroupSource",
    "HierarchyLevelSource",
    "LiteralSource",
    "MeasureSource",
    "Source",
]
