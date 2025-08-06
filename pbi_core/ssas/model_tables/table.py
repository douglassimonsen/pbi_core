import datetime
from typing import Optional
from uuid import UUID

from ..server.tabular_model import SsasRefreshTable
from .column import Column


class Table(SsasRefreshTable):
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

    def data(self, head: int = 100) -> list[int | float | str]:
        ret = self.tabular_model.server.query_dax(
            f"EVALUATE TOPN({head}, ALL('{self.name}'))",
            db_name=self.tabular_model.db_name,
        )
        return [next(iter(row.values())) for row in ret]

    def columns(self) -> list[Column]:
        return [column for column in self.tabular_model.columns if column.table_id == self.id]
