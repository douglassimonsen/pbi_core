import datetime
from typing import TYPE_CHECKING, Final

from attrs import field, setters

from pbi_core.attrs import define
from pbi_core.ssas.model_tables.base import SsasReadonlyRecord
from pbi_core.ssas.model_tables.enums import DataState

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables.base.base_ssas_table import SsasTable
    from pbi_core.ssas.model_tables.column import Column
    from pbi_core.ssas.model_tables.level import Level


@define()
class AttributeHierarchy(SsasReadonlyRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/93d1844f-a6c7-4dda-879b-2e26ed5cd297)
    """

    attribute_hierarchy_storage_id: int = field(eq=True)
    column_id: int = field(eq=True)
    state: Final[DataState] = field(eq=False, on_setattr=setters.frozen, default=DataState.READY)

    modified_time: Final[datetime.datetime] = field(eq=False, on_setattr=setters.frozen, repr=False)
    refreshed_time: Final[datetime.datetime] = field(eq=False, on_setattr=setters.frozen, repr=False)

    def pbi_core_name(self) -> str:
        """Returns the name displayed in the PBIX report."""
        return self.column().pbi_core_name()

    def column(self) -> "Column":
        return self._tabular_model.columns.find({"id": self.column_id})

    def levels(self) -> set["Level"]:
        return self._tabular_model.levels.find_all({"hierarchy_id": self.id})

    def children(self, *, recursive: bool = True) -> frozenset["SsasTable"]:
        base = frozenset(self.levels())
        if recursive:
            return self._recurse_children(base)
        return base

    def parents(self, *, recursive: bool = True) -> frozenset["SsasTable"]:
        base = frozenset({self.column()})
        if recursive:
            return self._recurse_parents(base)
        return base
