import inspect
from enum import IntEnum
from typing import Optional

from .._base_node import LayoutNode


class EntityType(IntEnum):
    NA = 1
    NA2 = 0


class Entity(LayoutNode):
    Entity: str
    Name: Optional[str] = None
    Type: Optional[EntityType] = EntityType.NA2

    def table(self) -> str:
        return self.Entity

    @staticmethod
    def create(entity: str) -> "Entity":  # type: ignore  # mypy is convinced we're returning the property Entity rather than the type
        return Entity.model_validate({"Entity": entity})

    def __repr__(self) -> str:
        return f"Entity({self.Entity})"


class Source(LayoutNode):
    Source: str

    def table(self) -> str:
        return self.Source


class SourceRef(LayoutNode):
    SourceRef: Entity | Source

    def table(self) -> str:
        return self.SourceRef.table()

    def column(self) -> str:
        return "NA"


class SourceExpression(LayoutNode):
    Expression: SourceRef
    Property: str

    def table(self) -> str:
        return self.Expression.table()

    def column(self) -> str:
        return self.Property

    @staticmethod
    def create(table: str, column: str) -> "SourceExpression":
        ret: "SourceExpression" = SourceExpression.model_validate({
            "Expression": {
                "SourceRef": Entity.create(entity=table).model_dump_json(),  # type: ignore
                "Property": column,
            }
        })
        return ret


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
