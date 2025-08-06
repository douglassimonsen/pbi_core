from enum import IntEnum
from typing import Optional

from .._base_node import LayoutNode
from .column import ColumnSource
from .hierarchy import HierarchyLevelSource
from .measure import MeasureSource

DataSource = ColumnSource | MeasureSource | HierarchyLevelSource


class AggregationFunction(IntEnum):
    SUM = 0
    AVERAGE = 1
    COUNT = 2
    MIN = 3
    MAX = 4
    DISTINCT_COUNT = 5
    MEDIAN = 6
    STD_DEV_P = 7
    VAR_P = 8


class _AggregationSourceHelper(LayoutNode):
    Expression: DataSource
    Function: AggregationFunction


class AggregationSource(LayoutNode):
    Aggregation: _AggregationSourceHelper
    Name: Optional[str] = None
    NativeReferenceName: Optional[str] = None  # only for Layout.Visual.Query
