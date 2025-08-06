import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from ..server.tabular_model import SsasTable
from ._base import SsasRenameCommands

if TYPE_CHECKING:
    from .model import Model
    from .query_group import QueryGroup


class Expression(SsasTable):
    _commands: SsasRenameCommands
    description: Optional[str] = None
    expression: str
    kind: int
    lineage_tag: UUID
    model_id: int
    name: str
    query_group_id: Optional[int] = None

    modified_time: datetime.datetime

    def model(self) -> "Model":
        return self.tabular_model.model

    def query_group(self) -> Optional["QueryGroup"]:
        return self.tabular_model.query_groups.find({"id": self.query_group_id})
