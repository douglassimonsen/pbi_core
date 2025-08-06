import datetime
from typing import TYPE_CHECKING, Any

from ...lineage import LineageNode, LineageType
from ..server.tabular_model import SsasBaseTable

if TYPE_CHECKING:
    from .culture import Culture


class LinguisticMetadata(SsasBaseTable):
    content: Any
    content_type: int
    culture_id: int

    modified_time: datetime.datetime

    def culture(self) -> "Culture":
        return self.tabular_model.cultures.find({"id": self.culture_id})

    @classmethod
    def _db_plural_type_name(cls) -> str:
        return "LinguisticMetadata"

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        else:
            return LineageNode(self, lineage_type, [self.culture().get_lineage(lineage_type)])
