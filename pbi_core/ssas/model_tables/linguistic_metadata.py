import datetime
from typing import TYPE_CHECKING, Any

from ..server.tabular_model import SsasTable

if TYPE_CHECKING:
    from .culture import Culture


class LinguisticMetadata(SsasTable):
    content: Any
    content_type: int
    culture_id: int

    modified_time: datetime.datetime

    def culture(self) -> "Culture":
        return self.tabular_model.cultures.get({"id": self.culture_id})
