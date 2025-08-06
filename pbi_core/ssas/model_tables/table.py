import datetime
from typing import Optional
from uuid import UUID

from ..server.tabular_model import SsasTable
from ._commands import SsasRefreshCommands


class Table(SsasTable):
    _commands: SsasRefreshCommands
    alternate_source_precedence: int
    data_category: Optional[str] = None
    description: Optional[str] = None
    exclude_from_model_refresh: bool
    is_hidden: bool
    is_private: bool
    lineage_tag: UUID
    model_id: str
    name: str
    show_as_variations_only: bool
    system_flags: int
    system_managed: Optional[bool] = None
    table_storage_id: Optional[int] = None

    modified_time: datetime.datetime
    structure_modified_time: datetime.datetime
