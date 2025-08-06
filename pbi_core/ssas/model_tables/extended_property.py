import datetime
from typing import Any

from pydantic import Json

from pbi_core.pydantic import BaseValidation
from pbi_core.ssas.server.tabular_model import SsasRenameRecord


class ExtendedPropertyValue(BaseValidation):
    version: int
    daxTemplateName: str | None = None  # noqa: N815
    groupedColumns: Any = None  # noqa: N815
    binningMetadata: Any = None  # noqa: N815


class ExtendedProperty(SsasRenameRecord):
    """TBD.

    SSAS spec: https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/5c1521e5-defe-4ba2-9558-b67457e94569
    """

    object_id: int
    object_type: int
    name: str
    type: int
    value: Json[ExtendedPropertyValue]
    modified_time: datetime.datetime

    @classmethod
    def _db_command_obj_name(cls) -> str:
        return "ExtendedProperties"
