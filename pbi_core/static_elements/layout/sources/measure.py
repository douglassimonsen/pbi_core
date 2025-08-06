import inspect
from typing import Any, Optional

from .._base_node import LayoutNode
from .base import SourceExpression


class MeasureSource(LayoutNode):
    Measure: SourceExpression
    Name: Optional[str] = None
    NativeReferenceName: Optional[str] = None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MeasureSource):
            return False
        return (self.Measure.column() == other.Measure.column()) and (self.Measure.table() == other.Measure.table())

    def __hash__(self) -> int:
        return hash((self.Measure.table(), self.Measure.column()))


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
