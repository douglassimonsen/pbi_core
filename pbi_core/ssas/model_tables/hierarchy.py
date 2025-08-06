import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasRenameRecord

if TYPE_CHECKING:
    from .level import Level
    from .table import Table
    from .variation import Variation


class Hierarchy(SsasRenameRecord):
    hide_members: int
    hierarchy_storage_id: int
    is_hidden: bool
    lineage_tag: UUID = uuid4()
    name: str
    state: int
    table_id: int

    modified_time: datetime.datetime
    refreshed_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.table_id})

    def levels(self) -> set["Level"]:
        return self.tabular_model.levels.find_all({"hierarchy_id": self.id})

    def variations(self) -> set["Variation"]:
        return self.tabular_model.variations.find_all({"default_hierarchy_id": self.id})

    @classmethod
    def _db_command_obj_name(cls) -> str:
        return "Hierarchies"

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(
                self,
                lineage_type,
                [level.get_lineage(lineage_type) for level in self.levels()]
                + [variation.get_lineage(lineage_type) for variation in self.variations()],
            )

        return LineageNode(
            self,
            lineage_type,
            [
                self.table().get_lineage(lineage_type),
            ],
        )
