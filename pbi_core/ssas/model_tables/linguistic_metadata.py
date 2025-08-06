import datetime
from typing import TYPE_CHECKING, Any

from ..server.tabular_model import SsasTable
from ._base import SsasBaseCommands

if TYPE_CHECKING:
    from .culture import Culture


class LinguisticMetadata(SsasTable):
    _commands: SsasBaseCommands
    content: Any
    content_type: int
    culture_id: int

    modified_time: datetime.datetime

    def culture(self) -> "Culture":
        return self.tabular_model.cultures.find({"id": self.culture_id})

    @classmethod
    def _db_plural_type_name(cls) -> str:
        return "LinguisticMetadata"
