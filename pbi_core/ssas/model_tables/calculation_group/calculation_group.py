import datetime
from typing import TYPE_CHECKING

from attrs import field

from pbi_core.attrs import define
from pbi_core.ssas.model_tables.base import SsasEditableRecord
from pbi_core.ssas.server._commands import BaseCommands
from pbi_core.ssas.server.utils import SsasCommands

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables.table import Table


@define()
class CalculationGroup(SsasEditableRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/ed9dcbcf-9910-455f-abc4-13c575157cfb)
    """

    description: str
    precedence: int
    table_id: int

    modified_time: datetime.datetime

    _commands: BaseCommands = field(factory=lambda: SsasCommands.calculation_group, init=False, repr=False)

    def modification_hash(self) -> int:
        return hash((
            self.description,
            self.precedence,
            self.table_id,
        ))

    def table(self) -> "Table":
        return self.tabular_model.tables.find(self.table_id)
