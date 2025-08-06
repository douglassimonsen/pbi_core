import datetime
from typing import Any

from pydantic import Json

from pbi_core.ssas.server.tabular_model import SsasRenameTable


class ExtendedProperty(SsasRenameTable):
    object_id: int
    object_type: int
    name: str
    type: int
    value: Json[Any]
    modified_time: datetime.datetime

    @classmethod
    def _db_command_obj_name(cls) -> str:
        return "ExtendedProperties"
