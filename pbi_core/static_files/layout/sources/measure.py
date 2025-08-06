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
