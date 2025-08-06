import datetime
from typing import TYPE_CHECKING

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasRenameRecord

if TYPE_CHECKING:
    from .column import Column
    from .model import Model
    from .table import Table
    from .variation import Variation


class Relationship(SsasRenameRecord):
    cross_filtering_behavior: int
    from_column_id: int
    from_cardinality: int
    from_table_id: int
    is_active: bool
    join_on_date_behavior: int
    model_id: int
    name: str
    relationship_storage_id: int | None = None

    relationship_storage2_id: int | None = None
    relationship_storage2id: int | None = None

    refreshed_time: datetime.datetime
    rely_on_referential_integrity: bool
    security_filtering_behavior: int
    state: int
    to_cardinality: int
    to_column_id: int
    to_table_id: int
    type: int

    modified_time: datetime.datetime

    def from_table(self) -> "Table":
        """Returns the table the relationship is using as a filter.

        Note:
        ----
            In the bi-directional case, this table is also filtered

        """
        return self.tabular_model.tables.find({"id": self.from_table_id})

    def to_table(self) -> "Table":
        """Returns the table the relationship is being filtered.

        Note:
        ----
            In the bi-directional case, this table is also used as a filter

        """
        return self.tabular_model.tables.find({"id": self.to_table_id})

    def from_column(self) -> "Column":
        """The column in the from_table used to join with the to_table."""
        return self.tabular_model.columns.find({"id": self.from_column_id})

    def to_column(self) -> "Column":
        """The column in the to_table used to join with the from_table."""
        return self.tabular_model.columns.find({"id": self.to_column_id})

    def model(self) -> "Model":
        """The DB model this entity exists in."""
        return self.tabular_model.model

    def variations(self) -> set["Variation"]:
        return self.tabular_model.variations.find_all({"relationship_id": self.id})

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(
                self,
                lineage_type,
                [variation.get_lineage(lineage_type) for variation in self.variations()],
            )
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
