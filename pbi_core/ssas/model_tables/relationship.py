import datetime
from typing import TYPE_CHECKING, Optional

from ...lineage import LineageNode, LineageType
from ..server.tabular_model import SsasRenameTable

if TYPE_CHECKING:
    from .column import Column
    from .model import Model
    from .table import Table
    from .variation import Variation


class Relationship(SsasRenameTable):
    cross_filtering_behavior: int
    from_column_id: int
    from_cardinality: int
    from_table_id: int
    is_active: bool
    join_on_date_behavior: int
    model_id: int
    name: str
    relationship_storage_id: Optional[int] = None
    relationship_storage2_id: Optional[int] = None
    refreshed_time: datetime.datetime
    rely_on_referential_integrity: bool
    security_filtering_behavior: int
    state: int
    to_cardinality: int
    to_column_id: int
    to_table_id: int
    type: int

    modified_time: datetime.datetime

    def lineage_name(self) -> str:
        return self.name

    def from_table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.from_table_id})

    def to_table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.to_table_id})

    def from_column(self) -> "Column":
        return self.tabular_model.columns.find({"id": self.from_column_id})

    def to_column(self) -> "Column":
        return self.tabular_model.columns.find({"id": self.to_column_id})

    def model(self) -> "Model":
        return self.tabular_model.model

    def variations(self) -> list["Variation"]:
        return self.tabular_model.variations.find_all({"relationship_id": self.id})

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(
                self, lineage_type, [variation.get_lineage(lineage_type) for variation in self.variations()]
            )
        else:
            return LineageNode(
                self,
                lineage_type,
                [
                    self.from_table().get_lineage(lineage_type),
                    self.to_table().get_lineage(lineage_type),
                    self.from_column().get_lineage(lineage_type),
                    self.to_column().get_lineage(lineage_type),
                ],
            )
