import inspect
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, Annotated, Any, Optional, Union

from pydantic import Discriminator, Json, Tag

from ._base_node import LayoutNode
from .filters import FilterExpression, VisualFilter
from .filters import OrderBy as Orderby
from .sources import Source
from .visuals import Visual

if TYPE_CHECKING:
    from .section import Section


class SingleVisualGroup(LayoutNode):
    displayName: str
    groupMode: int
    objects: Optional[Any] = None
    isHidden: bool = False


class VisualHowCreated(Enum):
    InsertVisualButton = "InsertVisualButton"


class VisualConfig(LayoutNode):
    parent: "VisualContainer"
    _name_field = "name"

    layouts: Optional[Any] = None
    name: Optional[str] = None
    parentGroupName: Optional[str] = None
    singleVisualGroup: Optional[SingleVisualGroup] = None
    singleVisual: Optional[Visual] = None  # split classes to handle the other cases
    howCreated: Optional[VisualHowCreated] = None


class ExecutionMetricsKind(IntEnum):
    NA = 1


class EntityType(IntEnum):
    Table = 0


class FromEntity(LayoutNode):
    Name: str
    Entity: str
    Type: EntityType


class QueryHelper(FilterExpression):
    Select: list[Source]
    OrderBy: Optional[list[Orderby]] = None


class PrimaryProjections(LayoutNode):
    Projections: list[int]
    Subtotal: Optional[int] = None


class BindingPrimary(LayoutNode):
    Groupings: list[PrimaryProjections]


class DataVolume(IntEnum):
    NA = 4


class PrimaryDataReduction(LayoutNode):
    Sample: dict


class DataReduction(LayoutNode):
    DataVolume: DataVolume
    Primary: PrimaryDataReduction


class Binding(LayoutNode):
    Primary: BindingPrimary
    Projections: list[int]
    DataReduction: Any
    Version: int


class QueryCommand1(LayoutNode):
    ExecutionMetricsKind: ExecutionMetricsKind
    Query: QueryHelper
    Binding: Binding


class QueryCommand2(LayoutNode):
    SemanticQueryDataShapeCommand: QueryCommand1


def get_query_command(v: Any) -> str:
    if isinstance(v, dict):
        if "SemanticQueryDataShapeCommand" in v.keys():
            return "QueryCommand2"
        elif "ExecutionMetricsKind" in v.keys():
            return "QueryCommand1"
        else:
            raise ValueError(f"Unknown Filter: {v.keys()}")
    else:
        return v.__class__.__name__


QueryCommand = Annotated[
    Union[
        Annotated[QueryCommand1, Tag("QueryCommand1")],
        Annotated[QueryCommand2, Tag("QueryCommand2")],
    ],
    Discriminator(get_query_command),
]


class Query(LayoutNode):
    Commands: list[QueryCommand]


class VisualContainer(LayoutNode):
    parent: "Section"
    _name_field = "name"

    x: float
    y: float
    z: float
    width: float
    height: float
    tabOrder: Optional[int] = None
    dataTransforms: Optional[Json[Any]] = None
    query: Optional[Json[Query]] = None
    filters: Json[list[VisualFilter]] = []
    config: Json[VisualConfig]
    id: Optional[int] = None

    @property
    def name(self) -> Optional[str]:
        if self.config.singleVisual is not None:
            return f"{self.config.singleVisual.visualType}(x={round(self.x, 2)}, y={round(self.y, 2)}, z={round(self.z, 2)})"
        return None


"""
woo boy. Why is this code here? Well, we want a parent attribute on the objects to make user navigation easier
This has to be a non-private attribute due to a bug in pydantic right now.
We know we'll add the parent attribute after pydantic does it's work, but we want mypy to think the parent is
always there. Therefore we check all objects with parents and make the default None so the "is_required" becomes False
https://github.com/pydantic/pydantic/blob/a764871df98c8932e9b7bc10d861053d110a99e4/pydantic/fields.py#L572
"""
for name, obj in list(globals().items()):
    if inspect.isclass(obj) and issubclass(obj, LayoutNode) and "parent" in obj.model_fields:
        obj.model_fields["parent"].default = None
