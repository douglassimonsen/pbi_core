import datetime
from enum import IntEnum

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasRenameTable, SsasTable


class ObjectType(IntEnum):
    MODEL = 1
    TABLE = 3
    COLUMN = 4
    MEASURE = 8
    HIERARCHY = 9
    UNKNOWN = 12
    EXPRESSION = 41
    QUERY_GROUP = 51


# TODO: remove Any
class Annotation(SsasRenameTable):
    object_id: int
    object_type: ObjectType
    name: str
    value: str | None = None

    modified_time: datetime.datetime

    def parent(self) -> "SsasTable":  # noqa: PLR0911
        """Returns the object the annotation is describing.

        Raises
        ------
            TypeError: When the Object Type doesn't map to a know SSAS entity type

        """
        match self.object_type:
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
                msg = "No Matching Object ID"
                raise TypeError(msg)

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        return LineageNode(self, lineage_type, [self.parent().get_lineage(lineage_type)])
