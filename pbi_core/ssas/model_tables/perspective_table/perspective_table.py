import datetime
from typing import TYPE_CHECKING

from attrs import field

from pbi_core.attrs import define
from pbi_core.ssas.model_tables.base import SsasEditableRecord
from pbi_core.ssas.server._commands import BaseCommands
from pbi_core.ssas.server.utils import SsasCommands

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables.perspective import Perspective
    from pbi_core.ssas.model_tables.table import Table


@define()
class PerspectiveTable(SsasEditableRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/06bc5956-20e3-4bd2-8e5f-68a200efc18b)
    """

    include_all: bool
    perspective_id: int
    table_id: int

    modified_time: datetime.datetime

    _commands: BaseCommands = field(factory=lambda: SsasCommands.perspective_table, init=False, repr=False)

    def modification_hash(self) -> int:
        return hash((
            self.include_all,
            self.perspective_id,
            self.table_id,
        ))

    def perspective(self) -> "Perspective":
        return self.tabular_model.perspectives.find(self.perspective_id)

    def table(self) -> "Table":
        return self.tabular_model.tables.find(self.table_id)
