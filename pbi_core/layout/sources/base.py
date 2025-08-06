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

    @property
    def table(self) -> str:
        return self.Entity

    @classmethod
    def create(cls, entity: str) -> "Entity":  # type: ignore
        ret: "Entity" = Entity.model_validate({"Entity": entity})
        return ret

    def __repr__(self) -> str:
        return f"Entity({self.Entity})"


class Source(LayoutNode):
    Source: str

    @property
    def table(self) -> str:
        return self.Source


class SourceRef(LayoutNode):
    SourceRef: Entity | Source

    @property
    def table(self) -> str:
        return self.SourceRef.table

    @property
    def column(self) -> str:
        return "NA"


class SourceExpression(LayoutNode):
    Expression: SourceRef
    Property: str

    @property
    def table(self) -> str:
        return self.Expression.table

    @property
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
