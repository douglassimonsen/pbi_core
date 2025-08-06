import inspect
from typing import Optional

from .._base_node import LayoutNode
from .base import SourceRef
from .column import ColumnSource


class _GroupSourceHelper(LayoutNode):
    parent: "GroupSource"

    Expression: SourceRef
    GroupedColumns: list[ColumnSource]
    Property: str


class GroupSource(LayoutNode):
    GroupRef: _GroupSourceHelper
    Name: Optional[str] = None

    def __repr__(self) -> str:
        table = self.GroupRef.Expression.table
        column = self.GroupRef.Property
        return f"GroupRef({table}.{column})"

    def filter_name(self) -> str:
        return self.GroupRef.Property


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
