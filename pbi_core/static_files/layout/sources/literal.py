import inspect
from datetime import datetime

from .._base_node import LayoutNode

PrimitiveValue = int | str | datetime | bool | None
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def parse_literal(literal_val: str) -> PrimitiveValue:
    if literal_val == "null":
        return None
    if literal_val in ("true", "false"):
        return literal_val == "true"
    if literal_val.endswith("L"):
        return int(literal_val[:-1])
    if literal_val.startswith("datetime"):
        return datetime.strptime(literal_val[9:-1], DATETIME_FORMAT)
    return literal_val[1:-1]


class _LiteralSourceHelper(LayoutNode):
    Value: str


class LiteralSource(LayoutNode):
    Literal: _LiteralSourceHelper

    def value(self) -> PrimitiveValue:
        return parse_literal(self.Literal.Value)

    def __repr__(self) -> str:
        return f"LiteralSource({self.Literal.Value})"


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
