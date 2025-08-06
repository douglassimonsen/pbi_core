from typing import Optional

from .._base_node import LayoutNode
from .base import SourceExpression


class ColumnSource(LayoutNode):
    Column: SourceExpression
    Name: Optional[str] = None  # only seen on a couple TopN filters

    def __repr__(self) -> str:
        return f"ColumnSource({self.Column.Expression.table}.{self.Column.Property})"

    def filter_name(self) -> str:
        return self.Column.Property
