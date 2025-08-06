import inspect
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
    NativeReferenceName: Optional[str] = None


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
