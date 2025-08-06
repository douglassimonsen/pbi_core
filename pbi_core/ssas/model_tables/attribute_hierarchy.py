import datetime
from typing import TYPE_CHECKING

from ..server.tabular_model import SsasTable
from ._base import NoCommands

if TYPE_CHECKING:
    from .column import Column


class AttributeHierarchy(SsasTable):
    _commands: NoCommands
    attribute_hierarchy_storage_id: int
    column_id: int
    state: int

    modified_time: datetime.datetime
    refreshed_time: datetime.datetime

    def column(self) -> "Column":
        return self.tabular_model.columns.find({"id": self.column_id})
