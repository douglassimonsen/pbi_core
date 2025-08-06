import datetime
from typing import Any, Optional

from pydantic import Json

from ..server.tabular_model import SsasTable
from ._base import SsasModelCommands


class Model(SsasTable):
    _commands: SsasModelCommands
    culture: str
    data_access_options: Json[dict[str, Any]]
    data_source_default_max_connections: int
    data_source_variables_override_behavior: int
    default_data_view: int
    default_mode: int
    default_powerbi_data_source_version: int
    discourage_composite_models: Optional[bool] = None
    discourage_implicit_measures: bool
    disable_auto_exists: Optional[int] = None
    force_unique_names: bool
    name: str
    source_query_culture: str
    structure_modified_time: datetime.datetime
    version: int

    modified_time: datetime.datetime

    @classmethod
    def _db_plural_type_name(cls) -> str:
        return "Model"
