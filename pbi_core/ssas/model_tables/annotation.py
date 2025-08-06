import datetime
from enum import IntEnum
from typing import Any, Optional

from ..server.tabular_model import SsasTable
from ._base import SsasRenameCommands


class ObjectType(IntEnum):
    MODEL = 1
    TABLE = 3
    COLUMN = 4
    MEASURE = 8
    HIERARCHY = 9
    UNKNOWN = 12
    EXPRESSION = 41
    QUERY_GROUP = 51


class Annotation(SsasTable):
    object_id: int
    object_type: ObjectType
    name: str
    value: Optional[Any] = None
    _commands: SsasRenameCommands

    modified_time: datetime.datetime

    def parent(self) -> "SsasTable":
        match self.object_type:
            # we have to have type: ignore because python doesn't consider list[child] to be a subtype of list[parent] :(
            case ObjectType.MODEL:
                return self.tabular_model.model
            case ObjectType.TABLE:
                vals = self.tabular_model.tables
            case ObjectType.COLUMN:
                vals = self.tabular_model.columns
            case ObjectType.MEASURE:
                vals = self.tabular_model.measures
            case ObjectType.HIERARCHY:
                vals = self.tabular_model.hierarchies
            case ObjectType.EXPRESSION:
                vals = self.tabular_model.expressions
            case ObjectType.QUERY_GROUP:
                vals = self.tabular_model.query_groups
            case _:
                raise ValueError("No Matching Object ID")

        return [x for x in vals if x.id == self.object_id][0]
