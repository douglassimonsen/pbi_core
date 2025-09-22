import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

from attrs import field

from pbi_core.attrs import BaseValidation, Json, define
from pbi_core.lineage import LineageNode
from pbi_core.ssas.model_tables.base import SsasEditableRecord
from pbi_core.ssas.server._commands import BaseCommands
from pbi_core.ssas.server.utils import SsasCommands

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables.culture import Culture


class ContentType(Enum):
    Xml = 0
    Json = 1


@define()
class EntityDefinitionBinding(BaseValidation):
    ConceptualEntity: str
    ConceptualProperty: str | None = None
    VariationSource: str | None = None
    VariationSet: str | None = None
    Hierarchy: str | None = None
    HierarchyLevel: str | None = None


@define()
class EntityDefinition(BaseValidation):
    Binding: EntityDefinitionBinding


class TermSourceType(Enum):
    External = "External"


@define()
class TermSource(BaseValidation):
    Type: TermSourceType | None = None
    Agent: str


class TermDefinitionState(Enum):
    Suggested = "Suggested"
    Generated = "Generated"
    Deleted = "Deleted"


class TermDefinitionType(Enum):
    Noun = "Noun"


@define()
class TermDefinition(BaseValidation):
    State: TermDefinitionState | None = None
    Source: TermSource | None = None
    Weight: float | None = None
    Type: TermDefinitionType | None = None
    LastModified: datetime.datetime | None = None


class VisibilityValue(Enum):
    Hidden = "Hidden"


class VisibilityState(Enum):
    Authored = "Authored"


@define()
class VisibilityType(BaseValidation):
    Value: VisibilityValue
    State: VisibilityState | None = None


class NameTypeType(Enum):
    Identifier = "Identifier"
    Name = "Name"


@define()
class LinguisticMetadataEntity(BaseValidation):
    Weight: float | None = None
    State: TermDefinitionState
    Terms: list[dict[str, TermDefinition]] | None = None
    Definition: EntityDefinition | None = None
    Binding: EntityDefinitionBinding | None = None
    SemanticType: str | None = None
    Visibility: VisibilityType | None = None
    Hidden: bool = False
    NameType: NameTypeType | None = None
    Units: list[str] = []


@define()
class RelationshipBinding(BaseValidation):
    ConceptualEntity: str


@define()
class PhrasingAttributeRole(BaseValidation):
    Role: str


class RelationshipPhrasingState(Enum):
    Generated = "Generated"


# TODO: Subtype
@define()
class PhrasingAttribute(BaseValidation):
    Adjective: PhrasingAttributeRole | None = None
    Measurement: PhrasingAttributeRole | None = None
    Object: PhrasingAttributeRole | None = None
    Subject: PhrasingAttributeRole | None = None
    Name: PhrasingAttributeRole | None = None

    PrepositionalPhrases: list[dict[str, Any]] = []
    Adjectives: list[dict[str, TermDefinition]] = []
    Antonyms: list[dict[str, TermDefinition]] = []
    Prepositions: list[dict[str, TermDefinition]] = []
    Verbs: list[dict[str, TermDefinition]] = []
    Nouns: list[dict[str, TermDefinition]] = []


@define()
class RelationshipPhrasing(BaseValidation):
    Name: PhrasingAttribute | None = None
    Attribute: PhrasingAttribute | None = None
    Verb: PhrasingAttribute | None = None
    Adjective: PhrasingAttribute | None = None
    Preposition: PhrasingAttribute | None = None
    DynamicAdjective: PhrasingAttribute | None = None
    State: RelationshipPhrasingState | None = None
    Weight: float | None = None


@define()
class RelationshipRoleEntity(BaseValidation):
    Entity: str


@define()
class RelationshipRole(BaseValidation):
    Target: RelationshipRoleEntity
    Nouns: Any | None = None


@define()
class SemanticSlot(BaseValidation):
    Where: PhrasingAttributeRole | None = None
    When: PhrasingAttributeRole | None = None


class ConditionOperator(Enum):
    Equals = "Equals"
    GreaterThan = "GreaterThan"


@define()
class Condition(BaseValidation):
    Target: PhrasingAttributeRole
    Operator: ConditionOperator
    Value: dict[str, list[int | str]]


@define()
class LinguisticMetadataRelationship(BaseValidation):
    Binding: RelationshipBinding
    Phrasings: list[RelationshipPhrasing] = []
    Roles: dict[str, RelationshipRole | int]
    State: str | None = None
    SemanticSlots: SemanticSlot | None = None
    Conditions: list[Condition] | None = None


@define()
class LinguisticMetadataContent(BaseValidation):
    Version: str  # SemanticVersion
    Language: str
    DynamicImprovement: str | None = None
    Relationships: dict[str, LinguisticMetadataRelationship] | None = None
    Entities: dict[str, LinguisticMetadataEntity] | None = None
    Examples: list[dict[str, dict[str, str]]] | None = None


@define()
class LinguisticMetadata(SsasEditableRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/f8924a45-70da-496a-947a-84b8d5beaae6)
    """

    content: Json[LinguisticMetadataContent]
    content_type: ContentType
    culture_id: int

    modified_time: datetime.datetime

    _commands: BaseCommands = field(factory=lambda: SsasCommands.linguistic_metadata, init=False, repr=False)

    def modification_hash(self) -> int:
        return hash((
            self.content.model_dump_json(),
            self.content_type,
            self.culture_id,
        ))

    def culture(self) -> "Culture":
        return self.tabular_model.cultures.find({"id": self.culture_id})

    def pbi_core_name(self) -> str:
        """Returns the name displayed in the PBIX report."""
        return self.culture().pbi_core_name()

    @classmethod
    def _db_command_obj_name(cls) -> str:
        return "LinguisticMetadata"

    def get_lineage(self, lineage_type: Literal["children", "parents"]) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        return LineageNode(self, lineage_type, [self.culture().get_lineage(lineage_type)])
