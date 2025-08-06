import datetime
from enum import IntEnum
from typing import Any, Optional

from ...lineage import LineageNode, LineageType
from ..server.tabular_model import SsasRenameTable, SsasTable


class ObjectType(IntEnum):
    MODEL = 1
    TABLE = 3
    COLUMN = 4
    MEASURE = 8
    HIERARCHY = 9
    UNKNOWN = 12
    EXPRESSION = 41
    QUERY_GROUP = 51


class Annotation(SsasRenameTable):
    object_id: int
    object_type: ObjectType
    name: str
    value: Optional[Any] = None

    modified_time: datetime.datetime

    def parent(self) -> "SsasTable":
        match self.object_type:
            # we have to have type: ignore because python doesn't consider list[child] to be a subtype of list[parent] :(
            case ObjectType.MODEL:
                return self.tabular_model.model
            case ObjectType.TABLE:
                return self.tabular_model.tables.find({"id": self.object_id})
            case ObjectType.COLUMN:
                return self.tabular_model.columns.find({"id": self.object_id})
            case ObjectType.MEASURE:
                return self.tabular_model.measures.find({"id": self.object_id})
            case ObjectType.HIERARCHY:
                return self.tabular_model.hierarchies.find({"id": self.object_id})
            case ObjectType.EXPRESSION:
                return self.tabular_model.expressions.find({"id": self.object_id})
            case ObjectType.QUERY_GROUP:
                return self.tabular_model.query_groups.find({"id": self.object_id})
            case _:
                raise ValueError("No Matching Object ID")

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        else:
            return LineageNode(self, lineage_type, [self.parent().get_lineage(lineage_type)])
