import datetime
from typing import TYPE_CHECKING, Final

from attrs import field, setters

from pbi_core.attrs import define
from pbi_core.ssas.model_tables.base import SsasEditableRecord
from pbi_core.ssas.model_tables.base.base_ssas_table import SsasTable
from pbi_core.ssas.server._commands import BaseCommands
from pbi_core.ssas.server.utils import SsasCommands

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables.base.base_ssas_table import SsasTable
    from pbi_core.ssas.model_tables.calculation_item.calculation_item import CalculationItem
    from pbi_core.ssas.model_tables.table import Table


@define()
class CalculationGroup(SsasEditableRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/ed9dcbcf-9910-455f-abc4-13c575157cfb)
    """

    description: str = field(eq=True, default="")
    precedence: int = field(eq=True)
    table_id: int = field(eq=True)

    modified_time: Final[datetime.datetime] = field(eq=False, on_setattr=setters.frozen, repr=False)

    _commands: BaseCommands = field(default=SsasCommands.calculation_group, init=False, repr=False, eq=False)

    def table(self) -> "Table":
        return self._tabular_model.tables.find(self.table_id)

    def calculation_items(self) -> "set[CalculationItem]":
        return self._tabular_model.calculation_items.find_all({"calculation_group_id": self.id})

    def parents(self, *, recursive: bool = True) -> frozenset["SsasTable"]:
        base = frozenset({self.table()})
        if recursive:
            return self._recurse_parents(base)
        return base

    def children(self, *, recursive: bool = False) -> frozenset["SsasTable"]:
        base = frozenset(self.calculation_items())
        if recursive:
            return self._recurse_children(base)
        return base
