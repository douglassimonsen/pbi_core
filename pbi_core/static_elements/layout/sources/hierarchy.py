import inspect
from typing import Optional

from .._base_node import LayoutNode
from .base import SourceExpression, SourceRef


class PropertyVariationSource(LayoutNode):
    Expression: SourceRef
    Name: str
    Property: str

    def column(self) -> str:
        return self.Property


class _PropertyVariationSourceHelper(LayoutNode):
    PropertyVariationSource: PropertyVariationSource

    def table(self) -> str:
        return self.PropertyVariationSource.Expression.table()

    def column(self) -> str:
        return self.PropertyVariationSource.column()


class _HierarchySourceHelper(LayoutNode):
    Expression: SourceExpression | _PropertyVariationSourceHelper | SourceRef
    Hierarchy: Optional[str] = None


class HierarchySource(LayoutNode):
    Hierarchy: _HierarchySourceHelper


class _HierarchyLevelSourceHelper(LayoutNode):
    parent: "HierarchyLevelSource"

    Expression: HierarchySource
    Level: Optional[str] = None


class HierarchyLevelSource(LayoutNode):
    HierarchyLevel: _HierarchyLevelSourceHelper
    Name: Optional[str] = None
    NativeReferenceName: Optional[str] = None

    def __repr__(self) -> str:
        table = self.HierarchyLevel.Expression.Hierarchy.Expression.table
        column = self.HierarchyLevel.Expression.Hierarchy.Expression.column
        level = self.HierarchyLevel.Level
        return f"HierarchyLevelSource({table}.{column}.{level})"


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
