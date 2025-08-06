import datetime
from typing import TYPE_CHECKING, Any

import pydantic
from pydantic_extra_types.semantic_version import SemanticVersion

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasBaseTable

if TYPE_CHECKING:
    from .culture import Culture


class LinguisticMetadataContent(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    Version: SemanticVersion
    Language: str
    DynamicImprovement: str | None = None
    Relationships: Any = None
    Entities: Any = None


class LinguisticMetadata(SsasBaseTable):
    content: pydantic.Json[LinguisticMetadataContent]
    content_type: int
    culture_id: int

    modified_time: datetime.datetime

    def culture(self) -> "Culture":
        return self.tabular_model.cultures.find({"id": self.culture_id})

    def pbi_core_name(self) -> str:
        return self.culture().pbi_core_name()

    @classmethod
    def _db_command_obj_name(cls) -> str:
        return "LinguisticMetadata"

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        return LineageNode(self, lineage_type, [self.culture().get_lineage(lineage_type)])
