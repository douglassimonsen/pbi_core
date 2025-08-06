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
    _parent: "HierarchyLevelSource"

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
