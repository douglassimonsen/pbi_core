from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict

from ....lineage import LineageNode, LineageType
from .._base_node import LayoutNode
from ..filters import PrototypeQuery
from ..sources.column import ColumnSource
from ..sources.measure import MeasureSource

if TYPE_CHECKING:
    from ....ssas.server import BaseTabularModel


class BaseVisual(LayoutNode):
    model_config = ConfigDict(extra="allow")

    objects: Any = None
    prototypeQuery: PrototypeQuery
    projections: Any = None
    hasDefaultSort: bool = False
    drillFilterOtherVisuals: bool = False
    vcObjects: Any
    visualType: str = "unknown"

    @property
    def id(self) -> str:
        """Obviously terrible, but works for now lol"""
        return self.visualType

    def pbi_core_name(self) -> str:
        return self.__class__.__name__

    def get_lineage(self, lineage_type: LineageType, tabular_model: "BaseTabularModel") -> LineageNode:
        ret = []
        table_mapping = self.prototypeQuery.table_mapping()
        children = self.prototypeQuery.dependencies()
        for child in children:
            if isinstance(child, ColumnSource):
                col_candidates = tabular_model.columns.find_all({"explicit_name": child.Column.column()})
                for candidate in col_candidates:
                    if candidate.table().name == table_mapping[child.Column.table()]:
                        ret.append(candidate)
                        break
            elif isinstance(child, MeasureSource):
                col_candidates = tabular_model.measures.find_all({"name": child.Measure.column()})
                for candidate in col_candidates:
                    if candidate.table().name == table_mapping[child.Measure.table()]:
                        ret.append(candidate)
                        break
        return LineageNode(self, lineage_type, relatives=[child.get_lineage(lineage_type) for child in ret])
