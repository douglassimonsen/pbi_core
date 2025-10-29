from typing import TYPE_CHECKING

from attrs import field

from pbi_core.attrs import define
from pbi_core.ssas.model_tables.base import SsasRenameRecord
from pbi_core.ssas.model_tables.base.base_ssas_table import SsasTable
from pbi_core.ssas.server import RenameCommands, SsasCommands

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables import Column, Hierarchy, Relationship, SsasTable


@define()
class Variation(SsasRenameRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/b9dfeb51-cbb6-4eab-91bd-fa2b23f51ca3)
    """

    column_id: int = field(eq=True)
    default_column_id: int | None = field(default=None, eq=True)
    default_hierarchy_id: int = field(eq=True)
    description: str | None = field(default=None, eq=True)
    is_default: bool = field(eq=True)
    name: str = field(eq=True)
    relationship_id: int = field(eq=True)

    _commands: RenameCommands = field(default=SsasCommands.variation, init=False, repr=False)

    def column(self) -> "Column":
        """Name is bad to not consistent with other methods because the column field in this entity :(."""
        return self._tabular_model.columns.find(self.column_id)

    def default_column(self) -> "Column | None":
        if self.default_column_id is None:
            return None
        return self._tabular_model.columns.find(self.default_column_id)

    def default_hierarchy(self) -> "Hierarchy":
        return self._tabular_model.hierarchies.find(self.default_hierarchy_id)

    def relationship(self) -> "Relationship":
        return self._tabular_model.relationships.find(self.relationship_id)

    def children(self, *, recursive: bool = True) -> frozenset["SsasTable"]:
        base = frozenset(self.annotations())
        if recursive:
            return self._recurse_children(base)
        return base

    def parents(self, *, recursive: bool = True) -> frozenset["SsasTable"]:
        base_deps = {self.default_hierarchy(), self.relationship(), self.column()}
        if dc := self.default_column():
            base_deps.add(dc)
        frozen_base_deps = frozenset(base_deps)
        if recursive:
            return self._recurse_children(frozen_base_deps)
        return frozen_base_deps
