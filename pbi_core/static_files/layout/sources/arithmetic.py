from enum import IntEnum

from pbi_core.static_files.layout._base_node import LayoutNode

from .aggregation import AggregationSource, DataSource


class ArithmeticOperator(IntEnum):
    DIVIDE = 3


class ScopedEval2(LayoutNode):
    Expression: AggregationSource | DataSource
    Scope: list[str]  # no values have been seen in this field


class ScopedEval(LayoutNode):
    ScopedEval: ScopedEval2


class _ArithmeticSourceHelper(LayoutNode):
    Left: AggregationSource | DataSource
    Right: ScopedEval
    Operator: ArithmeticOperator


class ArithmeticSource(LayoutNode):
    Arithmetic: _ArithmeticSourceHelper
    Name: str | None = None
