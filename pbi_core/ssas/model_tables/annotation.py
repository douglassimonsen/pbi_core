import datetime

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasRenameRecord, SsasTable

from .enums import ObjectType


class Annotation(SsasRenameRecord):
    """TBD.

    SSAS spec: https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/7a16a837-cb88-4cb2-a766-a97c4d0e1f43
    """

    object_id: int
    object_type: ObjectType
    name: str
    value: str | None = None

    modified_time: datetime.datetime

    def object(self) -> SsasTable:  # noqa: PLR0911
        """Returns the object the annotation is describing.

        Raises
        ------
            TypeError: When the Object Type doesn't map to a know SSAS entity type

        """
        match self.object_type:
            case ObjectType.MODEL:
                return self.tabular_model.model
            case ObjectType.DATASOURCE:
                return self.tabular_model.data_sources.find(self.object_id)
            case ObjectType.TABLE:
                return self.tabular_model.tables.find(self.object_id)
            case ObjectType.COLUMN:
                return self.tabular_model.columns.find(self.object_id)
            case ObjectType.ATTRIBUTE_HIERARCHY:
                return self.tabular_model.attribute_hierarchies.find(self.object_id)
            case ObjectType.PARTITION:
                return self.tabular_model.partitions.find(self.object_id)
            case ObjectType.RELATIONSHIP:
                return self.tabular_model.relationships.find(self.object_id)
            case ObjectType.MEASURE:
                return self.tabular_model.measures.find(self.object_id)
            case ObjectType.HIERARCHY:
                return self.tabular_model.hierarchies.find(self.object_id)
            case ObjectType.LEVEL:
                return self.tabular_model.levels.find(self.object_id)
            case ObjectType.KPI:
                return self.tabular_model.kpis.find(self.object_id)
            case ObjectType.CULTURE:
                return self.tabular_model.cultures.find(self.object_id)
            case ObjectType.LINGUISTIC_METADATA:
                return self.tabular_model.linguistic_metadata.find(self.object_id)
            case ObjectType.PERSPECTIVE:
                return self.tabular_model.perspectives.find(self.object_id)
            case ObjectType.PERSPECTIVE_TABLE:
                return self.tabular_model.perspective_tables.find(self.object_id)
            case ObjectType.PERSPECTIVE_HIERARCHY:
                return self.tabular_model.perspective_hierarchies.find(self.object_id)
            case ObjectType.PERSPECTIVE_MEASURE:
                return self.tabular_model.perspective_measures.find(self.object_id)
            case ObjectType.ROLE:
                return self.tabular_model.roles.find(self.object_id)
            case ObjectType.ROLE_MEMBERSHIP:
                return self.tabular_model.role_memberships.find(self.object_id)
            case ObjectType.TABLE_PERMISSION:
                return self.tabular_model.table_permissions.find(self.object_id)
            case ObjectType.VARIATION:
                return self.tabular_model.variations.find(self.object_id)
            case ObjectType.EXPRESSION:
                return self.tabular_model.expressions.find(self.object_id)
            case ObjectType.COLUMN_PERMISSION:
                return self.tabular_model.column_permissions.find(self.object_id)
            case ObjectType.CALCULATION_GROUP:
                return self.tabular_model.calculation_groups.find(self.object_id)
            case ObjectType.QUERY_GROUP:
                return self.tabular_model.query_groups.find(self.object_id)
            case _:
                msg = f"No logic implemented for type {self.object_type}"
                raise TypeError(msg)

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        return LineageNode(self, lineage_type, [self.parent().get_lineage(lineage_type)])
