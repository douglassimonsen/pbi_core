# ruff: noqa: N815
from enum import Enum, StrEnum
from typing import TYPE_CHECKING, Annotated, Any

from pydantic import ConfigDict, Discriminator, Tag

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.static_files.layout._base_node import LayoutNode
from pbi_core.static_files.layout.filters import Filter, PrototypeQuery
from pbi_core.static_files.layout.sources.column import ColumnSource
from pbi_core.static_files.layout.sources.measure import MeasureSource
from pbi_core.static_files.layout.visuals.properties import Expression

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables import Column, Measure
    from pbi_core.ssas.server import BaseTabularModel
    from pbi_core.static_files.model_references import ModelColumnReference, ModelMeasureReference


class FilterSortOrder(Enum):
    NA = 0
    NA1 = 1
    NA2 = 2
    NA3 = 3


class DisplayMode(Enum):
    hidden = "hidden"


class Display(LayoutNode):
    mode: DisplayMode


class ProjectionConfig(LayoutNode):
    queryRef: str
    active: bool = False
    suppressConcat: bool = False


class PropertyDefSelectorId(StrEnum):
    default = "default"
    hover = "hover"
    id = "id"
    selected = "selected"


class PropertyDefSelector(LayoutNode):
    id: PropertyDefSelectorId | None = None
    metadata: str | None = None


class ColorRule1(LayoutNode):
    positiveColor: Expression
    negativeColor: Expression
    axisColor: Expression
    reverseDirection: Expression
    hideText: Expression | None = None


def get_property_expression(v: object | dict[str, Any]) -> str:
    if isinstance(v, dict):
        if "positiveColor" in v:
            return "ColorRule1"
        if "filter" in v:
            return "Filter"
        return "Expression"
    return v.__class__.__name__


PropertyExpression = Annotated[
    Annotated[Expression, Tag("Expression")]
    | Annotated[Filter, Tag("Filter")]
    | Annotated[ColorRule1, Tag("ColorRule1")],
    Discriminator(get_property_expression),
]


class PropertyDef(LayoutNode):
    properties: dict[str, PropertyExpression]
    selector: PropertyDefSelector | None = None


class BaseVisual(LayoutNode):
    model_config = ConfigDict(extra="allow")

    objects: dict[str, list[PropertyDef]] = None
    prototypeQuery: PrototypeQuery | None = None
    projections: dict[str, list[ProjectionConfig]] | None = None
    hasDefaultSort: bool = False
    drillFilterOtherVisuals: bool = False
    filterSortOrder: FilterSortOrder = FilterSortOrder.NA
    # vcObjects means "visual container objects"
    vcObjects: int = None
    visualType: str = "unknown"
    queryOptions: int = None
    showAllRoles: int = None
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
