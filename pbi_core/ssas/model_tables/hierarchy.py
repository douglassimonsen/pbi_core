import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from ..server.tabular_model import SsasTable
from ._commands import SsasRenameCommands

if TYPE_CHECKING:
    from .level import Level
    from .table import Table
    from .variation import Variation


class Hierarchy(SsasTable):
    _commands: SsasRenameCommands
    hide_members: int
    hierarchy_storage_id: int
    is_hidden: bool
    lineage_tag: UUID
    name: str
    state: int
    table_id: int

    modified_time: datetime.datetime
    refreshed_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.table_id})

    def levels(self) -> list["Level"]:
        return self.tabular_model.levels.find_all({"hierarchy_id": self.id})

    def variations(self) -> list["Variation"]:
        return self.tabular_model.variations.find_all({"default_hierarchy_id": self.id})

    @classmethod
    def _db_plural_type_name(cls) -> str:
        return "Hierarchies"
