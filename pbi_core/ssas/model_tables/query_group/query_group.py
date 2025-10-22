from typing import TYPE_CHECKING

from attrs import field

from pbi_core.attrs import define
from pbi_core.ssas.model_tables.base import SsasEditableRecord
from pbi_core.ssas.server._commands import BaseCommands
from pbi_core.ssas.server.utils import SsasCommands

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables.base.base_ssas_table import SsasTable
    from pbi_core.ssas.model_tables.expression import Expression
    from pbi_core.ssas.model_tables.model import Model
    from pbi_core.ssas.model_tables.partition import Partition


@define()
class QueryGroup(SsasEditableRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/40b3830b-25ee-41a6-87d2-49616028dd13)
    This class represents a group of queries that can be executed together.
    """

    _repr_name_field = "folder"

    description: str | None = field(default=None, eq=True)
    folder: str = field(eq=True)
    model_id: int = field(eq=True)

    _commands: BaseCommands = field(default=SsasCommands.query_group, init=False, repr=False, eq=False)

    def expressions(self) -> set["Expression"]:
        return self._tabular_model.expressions.find_all({"query_group_id": self.id})

    def partitions(self) -> set["Partition"]:
        return self._tabular_model.partitions.find_all({"query_group_id": self.id})

    def model(self) -> "Model":
        return self._tabular_model.model

    def children(self, *, recursive: bool = True) -> frozenset["SsasTable"]:
        base_deps = frozenset(self.expressions() | self.partitions())
        if recursive:
            return self._recurse_children(base_deps)
        return base_deps

    def parents(self, *, recursive: bool = True) -> frozenset["SsasTable"]:
        base_deps = frozenset({self.model()})
        if recursive:
            return self._recurse_children(base_deps)
        return base_deps
