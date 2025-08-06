import datetime
from typing import TYPE_CHECKING

from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands

if TYPE_CHECKING:
    from .measure import Measure


class KPI(SsasTable):
    _commands: SsasBaseCommands
    measure_id: int
    status_expression: str
    status_graphic: str
    target_expression: str
    target_format_string: str

    modified_time: datetime.datetime

    def measure(self) -> "Measure":
        return self.tabular_model.measures.find({"id": self.measure_id})
