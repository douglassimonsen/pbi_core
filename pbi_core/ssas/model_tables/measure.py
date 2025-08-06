import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from ..server.tabular_model import SsasTable
from ._base import SsasRenameCommands

if TYPE_CHECKING:
    from .kpi import KPI
    from .table import Table


class Measure(SsasTable):
    _commands: SsasRenameCommands
    data_category: Optional[str] = None
    data_type: int
    description: Optional[str] = None
    display_folder: Optional[str] = None
    error_message: Optional[str] = None
    expression: Optional[str | int | float] = None
    format_string: Optional[str | int] = None
    is_hidden: bool
    is_simple_measure: bool
    kpi_id: Optional[int] = None
    lineage_tag: UUID
    name: str
    state: int
    table_id: int

    modified_time: datetime.datetime
    structure_modified_time: datetime.datetime

    def KPI(self) -> Optional["KPI"]:
        return self.tabular_model.kpis.find({"id": self.kpi_id})

    def table(self) -> "Table":
        return self.tabular_model.tables.find({"id": self.table_id})
