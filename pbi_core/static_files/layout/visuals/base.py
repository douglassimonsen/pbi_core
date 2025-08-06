# ruff: noqa: N815
from enum import Enum
from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.filters import PrototypeQuery
from pbi_core.static_files.layout.sources.column import ColumnSource
from pbi_core.static_files.layout.sources.measure import MeasureSource

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables import Column, Measure
    from pbi_core.ssas.server import BaseTabularModel
    from pbi_core.static_files.model_references import ModelColumnReference, ModelMeasureReference


class FilterSortOrder(Enum):
    NA = 1
    NA2 = 2
    NA3 = 3


class DisplayMode(Enum):
    hidden = "hidden"


class Display(LayoutNode):
    mode: DisplayMode


# TODO: remove Anys
class BaseVisual(LayoutNode):
    model_config = ConfigDict(extra="allow")

    objects: Any = None
    prototypeQuery: PrototypeQuery | None = None
    projections: Any = None
    hasDefaultSort: bool = False
    drillFilterOtherVisuals: bool = False
    filterSortOrder: FilterSortOrder = FilterSortOrder.NA
    vcObjects: Any = None
    visualType: str = "unknown"
    queryOptions: Any = None
    showAllRoles: Any = None
    display: Display | None = None

    @property
    def id(self) -> str:
        """Obviously terrible, but works for now lol."""
        return self.visualType

    def pbi_core_name(self) -> str:
        """Returns the name displayed in the PBIX report."""
        return self.__class__.__name__

    def get_ssas_elements(self) -> "set[ModelColumnReference | ModelMeasureReference]":
        if self.prototypeQuery is None:
            return set()
        return self.prototypeQuery.get_ssas_elements()

    def get_lineage(self, lineage_type: LineageType, tabular_model: "BaseTabularModel") -> LineageNode:
        ret: list[Column | Measure] = []
        if self.prototypeQuery is None:
            return LineageNode(self, lineage_type, [])
        table_mapping = self.prototypeQuery.table_mapping()
        children = self.prototypeQuery.get_ssas_elements()
        for child in children:
            if isinstance(child, ColumnSource):
                candidate_columns = tabular_model.columns.find_all({"explicit_name": child.Column.column()})
                for candidate_column in candidate_columns:
                    if candidate_column.table().name == table_mapping[child.Column.table()]:
                        ret.append(candidate_column)
                        break
            elif isinstance(child, MeasureSource):
                candidate_measures = tabular_model.measures.find_all({"name": child.Measure.column()})
                for candidate_measure in candidate_measures:
                    if candidate_measure.table().name == table_mapping[child.Measure.table()]:
                        ret.append(candidate_measure)
                        break
        return LineageNode(self, lineage_type, relatives=[child.get_lineage(lineage_type) for child in ret])
