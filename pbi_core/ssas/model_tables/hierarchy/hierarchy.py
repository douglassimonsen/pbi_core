import datetime
from typing import TYPE_CHECKING, Final
from uuid import UUID, uuid4

from attrs import field, setters

from pbi_core.attrs import define
from pbi_core.ssas.model_tables.base import SsasRenameRecord
from pbi_core.ssas.model_tables.base.lineage import LinkedEntity
from pbi_core.ssas.model_tables.enums import DataState
from pbi_core.ssas.server import RenameCommands, SsasCommands
from pbi_core.static_files.layout.sources.hierarchy import HierarchySource

from . import set_name
from .enums import HideMembers

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables import Level, PerspectiveHierarchy, Table, Variation
    from pbi_core.static_files.layout import Layout


@define()
class Hierarchy(SsasRenameRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/4eff6661-1458-4c5a-9875-07218f1458e5)
    """

    description: str | None = field(default=None, eq=True)
    display_folder: str | None = field(default=None, eq=True)
    hide_members: HideMembers = field(eq=True)
    hierarchy_storage_id: int = field(eq=True)
    is_hidden: bool = field(eq=True)
    name: str = field(eq=True)
    state: Final[DataState] = field(eq=False, on_setattr=setters.frozen, default=DataState.READY)
    table_id: int = field(eq=True)
    """A foreign key to the Table object the hierarchy is stored under"""

    lineage_tag: UUID = field(factory=uuid4, eq=True, repr=False)
    source_lineage_tag: UUID = field(factory=uuid4, eq=True, repr=False)

    modified_time: Final[datetime.datetime] = field(eq=False, on_setattr=setters.frozen, repr=False)
    refreshed_time: Final[datetime.datetime] = field(eq=False, on_setattr=setters.frozen, repr=False)
    """The last time the sources for this hierarchy were refreshed"""
    structure_modified_time: Final[datetime.datetime] = field(eq=False, on_setattr=setters.frozen, repr=False)

    _commands: RenameCommands = field(default=SsasCommands.hierarchy, init=False, repr=False, eq=False)

    def set_name(self, new_name: str, layout: "Layout") -> None:
        """Renames the measure and update any dependent expressions to use the new name.

        Since measures are referenced by name in DAX expressions, renaming a measure will break any dependent
        expressions.
        """
        hierarchies = layout.find_all(HierarchySource, lambda h: h.Hierarchy.Hierarchy == self.name)
        for h in hierarchies:
            h.Hierarchy.Hierarchy = new_name

        # no set_name for hierarchies like tables, columns, and measures since hierarchies are not directly referenced
        # in DAX
        set_name.fix_dax(self, new_name)
        self.name = new_name

    def table(self) -> "Table":
        return self._tabular_model.tables.find({"id": self.table_id})

    def levels(self) -> set["Level"]:
        return self._tabular_model.levels.find_all({"hierarchy_id": self.id})

    def variations(self) -> set["Variation"]:
        return self._tabular_model.variations.find_all({"default_hierarchy_id": self.id})

    def perspective_hierarchies(self) -> set["PerspectiveHierarchy"]:
        return self._tabular_model.perspective_hierarchies.find_all({"hierarchy_id": self.id})

    def children_base(self) -> frozenset["LinkedEntity"]:
        return (
            LinkedEntity.from_iter(self.levels(), by="level")
            | LinkedEntity.from_iter(
                self.variations(),
                by="variation",
            )
            | LinkedEntity.from_iter(
                self.perspective_hierarchies(),
                by="perspective_hierarchy",
            )
            | LinkedEntity.from_iter(self.annotations(), by="annotation")
        )

    def parents_base(self) -> frozenset["LinkedEntity"]:
        return LinkedEntity.from_iter({self.table()}, by="table")
