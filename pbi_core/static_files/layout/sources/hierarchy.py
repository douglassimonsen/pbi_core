from typing import TYPE_CHECKING

from pbi_core.static_files.layout._base_node import LayoutNode

from .base import SourceExpression, SourceRef

if TYPE_CHECKING:
    from pbi_core.static_files.layout.filters import From


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
    Hierarchy: str | None = None


class HierarchySource(LayoutNode):
    Hierarchy: _HierarchySourceHelper


class _HierarchyLevelSourceHelper(LayoutNode):
    _parent: "HierarchyLevelSource"

    Expression: HierarchySource
    Level: str | None = None


class HierarchyLevelSource(LayoutNode):
    HierarchyLevel: _HierarchyLevelSourceHelper
    Name: str | None = None
    NativeReferenceName: str | None = None

    def __repr__(self) -> str:
        table = self.HierarchyLevel.Expression.Hierarchy.Expression.table()
        column = self.HierarchyLevel.Expression.Hierarchy.Expression.column()
        level = self.HierarchyLevel.Level
        return f"HierarchyLevelSource({table}.{column}.{level})"

    def to_query_text(self, target_tables: dict[str, "From"]) -> str:
        raise NotImplementedError
