from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from .._base_node import LayoutNode

if TYPE_CHECKING:
    from ..filters import From


class EntityType(IntEnum):
    NA = 1
    NA2 = 0
    NA3 = 2


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
        return f"Entity({self.Name}: {self.Entity})"


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

    def to_query_text(self, target_tables: dict[str, "From"]):
        table_name: str = target_tables[self.table()].Entity  # type: ignore
        column_name: str = self.column()  # type: ignore
        return f"'{table_name}'[{column_name}]"

    @staticmethod
    def create(table: str, column: str) -> "SourceExpression":
        ret: "SourceExpression" = SourceExpression.model_validate({
            "Expression": {
                "SourceRef": Entity.create(entity=table).model_dump_json(),  # type: ignore
                "Property": column,
            }
        })
        return ret
