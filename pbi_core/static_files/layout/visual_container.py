# ruff: noqa: N815
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, Annotated, Any, cast

from pydantic import Discriminator, Json, Tag

from ._base_node import LayoutNode
from .filters import PrototypeQuery, PrototypeQueryResult, VisualFilter
from .visuals.main import Visual

if TYPE_CHECKING:
    from pbi_core.ssas.server import LocalTabularModel

    from .section import Section


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


class PrimaryProjections(LayoutNode):
    Projections: list[int]
    SuppressedProjections: list[int] | None = None
    Subtotal: int | None = None


class BindingPrimary(LayoutNode):
    Groupings: list[PrimaryProjections]
    Expansion: Any | None = None


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


class VisualContainer(LayoutNode):
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
    filters: Json[list[VisualFilter]] = []
    config: Json[VisualConfig]
    id: int | None = None

    def name(self) -> str | None:
        if self.config.singleVisual is not None:
            return f"{self.config.singleVisual.visualType}(x={round(self.x, 2)}, y={round(self.y, 2)}, z={round(self.z, 2)})"  # noqa: E501
        return None

    def get_data(self, model: "LocalTabularModel") -> PrototypeQueryResult | None:
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
        return query.get_data(model)
