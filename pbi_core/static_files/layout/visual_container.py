# ruff: noqa: N815
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, Annotated, Any, cast

from pydantic import Discriminator, Json, Tag

from pbi_core.lineage.main import LineageNode, LineageType
from pbi_core.static_files.model_references import ModelColumnReference, ModelMeasureReference

from ._base_node import LayoutNode
from .filters import PrototypeQuery, PrototypeQueryResult, VisualFilter
from .visuals.main import Visual

if TYPE_CHECKING:
    from pbi_core.ssas.server import LocalTabularModel
    from pbi_core.ssas.server.tabular_model.tabular_model import BaseTabularModel

    from .section import Section


from .performance import Performance, get_performance


class SingleVisualGroup(LayoutNode):
    displayName: str
    groupMode: int
    objects: Any | None = None
    isHidden: bool = False


class VisualHowCreated(Enum):
    InsertVisualButton = "InsertVisualButton"


class VisualConfig(LayoutNode):
    _parent: "VisualContainer"  # pyright: ignore reportIncompatibleVariableOverride=false
    _name_field = "name"

    layouts: Any | None = None
    name: str | None = None
    parentGroupName: str | None = None
    singleVisualGroup: SingleVisualGroup | None = None
    singleVisual: Visual | None = None  # split classes to handle the other cases
    howCreated: VisualHowCreated | None = None


class ExecutionMetricsKindEnum(IntEnum):
    NA = 1


class EntityType(IntEnum):
    Table = 0


class FromEntity(LayoutNode):
    Name: str
    Entity: str
    Type: EntityType


# TODO: remove Anys
class PrimaryProjections(LayoutNode):
    Projections: list[int]
    SuppressedProjections: list[int] | None = None
    Subtotal: int | None = None
    Aggregates: Any | None = None
    ShowItemsWithNoData: list[int] | None = None


class BindingPrimary(LayoutNode):
    Groupings: list[PrimaryProjections]
    Expansion: Any | None = None
    Synchronization: Any | None = None


class DataVolume(IntEnum):
    NA = 4


class PrimaryDataReduction(LayoutNode):
    Sample: dict[str, Any]


class DataReduction(LayoutNode):
    DataVolume: DataVolume
    Primary: PrimaryDataReduction


class QueryBinding(LayoutNode):
    IncludeEmptyGroups: bool = False
    Primary: BindingPrimary
    Secondary: BindingPrimary | None = None
    Projections: list[int] = []
    DataReduction: Any = None
    Aggregates: Any = None
    SuppressedJoinPredicates: Any = None
    Highlights: Any = None
    Version: int


class QueryCommand1(LayoutNode):
    ExecutionMetricsKind: ExecutionMetricsKindEnum = ExecutionMetricsKindEnum.NA
    Query: PrototypeQuery
    Binding: QueryBinding | None = None


class QueryCommand2(LayoutNode):
    SemanticQueryDataShapeCommand: QueryCommand1


def get_query_command(v: Any) -> str:
    if isinstance(v, dict):
        if "SemanticQueryDataShapeCommand" in v:
            return "QueryCommand2"
        if "ExecutionMetricsKind" in v:
            return "QueryCommand1"
        msg = f"Unknown Filter: {v.keys()}"
        raise ValueError(msg)
    return cast("str", v.__class__.__name__)


QueryCommand = Annotated[
    Annotated[QueryCommand1, Tag("QueryCommand1")] | Annotated[QueryCommand2, Tag("QueryCommand2")],
    Discriminator(get_query_command),
]


class Query(LayoutNode):
    Commands: list[QueryCommand]

    def get_ssas_elements(self) -> set[ModelColumnReference | ModelMeasureReference]:
        """Returns the SSAS elements (columns and measures) this query is directly dependent on."""
        ret: set[ModelColumnReference | ModelMeasureReference] = set()
        for command in self.Commands:
            if isinstance(command, QueryCommand1):
                ret.update(command.Query.get_ssas_elements())
            elif isinstance(command, QueryCommand2):
                ret.update(command.SemanticQueryDataShapeCommand.Query.get_ssas_elements())
        return ret


class VisualContainer(LayoutNode):
    """A Container for visuals in a report page.

    Generally, this is 1-1 with a real visual (bar chart, etc.), but can contain 0 (text boxes) or >1.
    It's at this level that the report connects with the SSAS model to get data for each visual.
    """

    _parent: "Section"  # pyright: ignore reportIncompatibleVariableOverride=false
    _name_field = "name"

    x: float
    y: float
    z: float
    width: float
    height: float
    tabOrder: int | None = None
    dataTransforms: Json[Any] | None = None
    query: Json[Query] | None = None
    queryHash: int | None = None
    filters: Json[list[VisualFilter]] = []
    config: Json[VisualConfig]
    id: int | None = None

    def pbi_core_name(self) -> str:
        viz = self.config.singleVisual
        assert viz is not None
        return viz.visualType

    def name(self) -> str | None:
        if self.config.singleVisual is not None:
            return f"{self.config.singleVisual.visualType}(x={round(self.x, 2)}, y={round(self.y, 2)}, z={round(self.z, 2)})"  # noqa: E501
        return None

    def _get_data_command(self) -> PrototypeQuery | None:
        if self.query is None:
            return None
        if len(self.query.Commands) == 0:
            return None

        if len(self.query.Commands) > 1:
            msg = "Cannot get data for multiple commands"
            raise NotImplementedError(msg)

        query_command = self.query.Commands[0]
        if isinstance(query_command, QueryCommand1):
            query = query_command.Query
        else:
            query = query_command.SemanticQueryDataShapeCommand.Query
        return query

    def get_data(self, model: "LocalTabularModel") -> PrototypeQueryResult | None:
        """Gets data that would populate this visual from the SSAS DB.

        Uses the PrototypeQuery found within query to generate a DAX statement that then gets passed to SSAS.

        Returns None for non-data visuals such as static text boxes

        """
        query = self._get_data_command()
        if query is None:
            return None
        return query.get_data(model)

    def get_performance(self, model: "LocalTabularModel") -> Performance:
        """Calculates various metrics on the speed of the visual.

        Current Metrics:
            Total Seconds to Query
            Total Rows Retrieved
        """
        command = self._get_data_command()
        if command is None:
            msg = "Cannot get performance for a visual without a query command"
            raise NotImplementedError(msg)
        return get_performance(model, [command.get_dax(model).DaxExpression])[0]

    def get_ssas_elements(self) -> set[ModelColumnReference | ModelMeasureReference]:
        """Returns the SSAS elements (columns and measures) this visual is directly dependent on."""
        ret: set[ModelColumnReference | ModelMeasureReference] = set()
        if self.config.singleVisual is not None:
            ret.update(self.config.singleVisual.get_ssas_elements())
        if self.query is not None:
            ret.update(self.query.get_ssas_elements())
        for f in self.filters:
            ret.update(f.get_ssas_elements())
        return ret

    # TODO: replace ._parent with a get_parent method
    def get_lineage(self, lineage_type: LineageType, tabular_model: "BaseTabularModel") -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)

        viz_entities = self.get_ssas_elements()
        page_filters = self._parent.get_ssas_elements(include_visuals=False)
        report_filters = self._parent._parent.get_ssas_elements(include_sections=False)
        entities = viz_entities | page_filters | report_filters
        children_nodes = [ref.to_model(tabular_model) for ref in entities]

        children_lineage = [p.get_lineage(lineage_type) for p in children_nodes if p is not None]
        return LineageNode(self, lineage_type, children_lineage)
