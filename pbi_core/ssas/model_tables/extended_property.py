import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Json

from pbi_core.ssas.server.tabular_model import SsasRenameTable


class ExtendedPropertyValue(BaseModel):
    version: int
    daxTemplateName: str | None = None  # noqa: N815
    groupedColumns: Any = None  # noqa: N815
    binningMetadata: Any = None  # noqa: N815

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )


class ExtendedProperty(SsasRenameTable):
    object_id: int
    object_type: int
    name: str
    type: int
    value: Json[ExtendedPropertyValue]
    modified_time: datetime.datetime

    @classmethod
    def _db_command_obj_name(cls) -> str:
        return "ExtendedProperties"
