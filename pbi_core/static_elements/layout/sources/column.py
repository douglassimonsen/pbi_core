import inspect
from typing import Any, Optional

from .._base_node import LayoutNode
from .base import SourceExpression


class ColumnSource(LayoutNode):
    Column: SourceExpression
    Name: Optional[str] = None  # only seen on a couple TopN filters
    NativeReferenceName: Optional[str] = None  # only for Layout.Visual.Query

    def __repr__(self) -> str:
        return f"ColumnSource({self.Column.Expression.table()}.{self.Column.Property})"

    def filter_name(self) -> str:
        return self.Column.Property

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ColumnSource):
            return False
        return (self.Column.column() == other.Column.column()) and (self.Column.table() == other.Column.table())

    def __hash__(self) -> int:
        return hash((self.Column.column(), self.Column.table()))


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
