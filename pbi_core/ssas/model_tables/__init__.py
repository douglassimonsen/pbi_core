import typing

if typing.TYPE_CHECKING:
    from ..server.tabular_model import SsasTable

from ._group import Group as Group
from .alternate_of import AlternateOf as AlternateOf
from .annotation import Annotation as Annotation
from .attribute_hierarchy import AttributeHierarchy as AttributeHierarchy
from .calculation_group import CalculationGroup as CalculationGroup
from .calculation_item import CalculationItem as CalculationItem
from .column import Column as Column
from .column_permission import ColumnPermission as ColumnPermission
from .culture import Culture as Culture
from .detail_row_definition import DetailRowDefinition as DetailRowDefinition
from .expression import Expression as Expression
from .extended_property import ExtendedProperty as ExtendedProperty
from .format_string_definition import FormatStringDefinition as FormatStringDefinition
from .group_by_column import GroupByColumn as GroupByColumn
from .hierarchy import Hierarchy as Hierarchy
from .kpi import Kpi as Kpi
from .level import Level as Level
from .linguistic_metadata import LinguisticMetadata as LinguisticMetadata
from .measure import Measure as Measure
from .model import Model as Model
from .object_translation import ObjectTranslation as ObjectTranslation
from .partition import Partition as Partition
from .perspective import Perspective as Perspective
from .perspective_column import PerspectiveColumn as PerspectiveColumn
from .perspective_hierarchy import PerspectiveHierarchy as PerspectiveHierarchy
from .perspective_measure import PerspectiveMeasure as PerspectiveMeasure
from .perspective_set import PerspectiveSet as PerspectiveSet
from .perspective_table import PerspectiveTable as PerspectiveTable
from .query_group import QueryGroup as QueryGroup
from .refresh_policy import RefreshPolicy as RefreshPolicy
from .related_column_detail import RelatedColumnDetail as RelatedColumnDetail
from .relationship import Relationship as Relationship
from .role import Role as Role
from .role_membership import RoleMembership as RoleMembership
from .set import Set as Set
from .table import Table as Table
from .table_permission import TablePermission as TablePermission
from .variation import Variation as Variation

FIELD_TYPES: dict[str, type["SsasTable"]] = {"annotations": Annotation, "tables": Table}
