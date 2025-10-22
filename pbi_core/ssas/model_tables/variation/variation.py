from typing import TYPE_CHECKING

from attrs import field

from pbi_core.attrs import define
from pbi_core.ssas.model_tables.base import SsasRenameRecord
from pbi_core.ssas.server._commands import RenameCommands
from pbi_core.ssas.server.utils import SsasCommands

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables.base.base_ssas_table import SsasTable
    from pbi_core.ssas.model_tables.column import Column
    from pbi_core.ssas.model_tables.hierarchy import Hierarchy
    from pbi_core.ssas.model_tables.relationship import Relationship


@define()
class Variation(SsasRenameRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/b9dfeb51-cbb6-4eab-91bd-fa2b23f51ca3)
    """

    column: int | None = field(default=None, eq=True)  # TODO: pbi says this shouldn't exist
    column_id: int = field(eq=True)
    default_column_id: int | None = field(default=None, eq=True)
    default_hierarchy_id: int = field(eq=True)
    description: str | None = field(default=None, eq=True)
    is_default: bool = field(eq=True)
    name: str = field(eq=True)
    relationship_id: int = field(eq=True)

    _commands: RenameCommands = field(default=SsasCommands.variation, init=False, repr=False)

    def get_column(self) -> "Column":
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

    def children(self, *, recursive: bool = True) -> frozenset["SsasTable"]:  # noqa: ARG002, PLR6301
        return frozenset()

    def parents(self, *, recursive: bool = True) -> frozenset["SsasTable"]:
        base_deps = {self.default_hierarchy(), self.relationship(), self.get_column()}
        default_column = self.default_column()
        if default_column:
            base_deps.add(default_column)
        frozen_base_deps = frozenset(base_deps)
        if recursive:
            return self._recurse_children(frozen_base_deps)
        return frozen_base_deps
