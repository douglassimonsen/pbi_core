import datetime
from typing import TYPE_CHECKING, Any, Optional

from pydantic import Json

from pbi_core.lineage import LineageNode, LineageType

from ..server.tabular_model import SsasModelTable

if TYPE_CHECKING:
    from .culture import Culture
    from .query_group import QueryGroup
    from .table import Table


class Model(SsasModelTable):
    culture: str
    data_access_options: Json[dict[str, Any]]
    data_source_default_max_connections: int
    data_source_variables_override_behavior: int
    default_data_view: int
    default_mode: int
    default_powerbi_data_source_version: int
    discourage_composite_models: Optional[bool] = None
    discourage_implicit_measures: bool
    disable_auto_exists: Optional[int] = None
    force_unique_names: bool
    name: str
    source_query_culture: str
    structure_modified_time: datetime.datetime
    version: int

    modified_time: datetime.datetime

    def lineage_name(self) -> str:
        return self.name

    def cultures(self) -> list["Culture"]:
        return self.tabular_model.cultures.find_all({"model_id": self.id})

    def tables(self) -> list["Table"]:
        return self.tabular_model.tables.find_all({"model_id": self.id})

    def query_groups(self) -> list["QueryGroup"]:
        return self.tabular_model.query_groups.find_all({"model_id": self.id})

    @classmethod
    def _db_plural_type_name(cls) -> str:
        return "Model"

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(
                self,
                lineage_type,
                [c.get_lineage(lineage_type) for c in self.cultures()]
                + [t.get_lineage(lineage_type) for t in self.tables()]
                + [q.get_lineage(lineage_type) for q in self.query_groups()],
            )
        else:
            return LineageNode(self, lineage_type)
