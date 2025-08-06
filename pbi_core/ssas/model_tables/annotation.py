import datetime
from enum import IntEnum

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasRenameRecord, SsasTable


class ObjectType(IntEnum):
    MODEL = 1
    DATASOURCE = 2
    TABLE = 3
    COLUMN = 4
    ATTRIBUTE_HIERARCHY = 5
    PARTITION = 6
    RELATIONSHIP = 7
    MEASURE = 8
    HIERARCHY = 9
    LEVEL = 10
    KPI = 12
    CULTURE = 13
    LINGUISTIC_METADATA = 15
    PERSPECTIVE = 29
    PERSPECTIVE_TABLE = 30
    PERSPECTIVE_COLUMN = 31
    PERSPECTIVE_HIERARCHY = 32
    PERSPECTIVE_MEASURE = 33
    ROLE = 34
    ROLE_MEMBERSHIP = 35
    TABLE_PERMISSION = 36
    VARIATION = 37
    EXPRESSION = 41
    COLUMN_PERMISSION = 42
    CALCULATION_GROUP = 46
    QUERY_GROUP = 51


# TODO: remove Any
class Annotation(SsasRenameRecord):
    """TBD.

    SSAS spec: https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/7a16a837-cb88-4cb2-a766-a97c4d0e1f43
    """

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
