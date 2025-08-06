import datetime
from typing import TYPE_CHECKING, Any

import pydantic
from pydantic_extra_types.semantic_version import SemanticVersion

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.ssas.server.tabular_model import SsasBaseTable

if TYPE_CHECKING:
    from .culture import Culture


class EntityDefinitionBinding(pydantic.BaseModel):
    ConceptualEntity: str
    ConceptualProperty: str | None = None
    VariationSource: str | None = None
    VariationSet: str | None = None
    Hierarchy: str | None = None
    HierarchyLevel: str | None = None

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )


class EntityDefinition(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    Binding: EntityDefinitionBinding


class TermSource(pydantic.BaseModel):
    Type: str | None = None  # TODO: enum
    Agent: str

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )


class TermDefinition(pydantic.BaseModel):
    State: str  # TODO: enum
    Source: TermSource
    Weight: float
    Type: str | None = None  # TODO: enum

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )


class LinguisticMetadataEntity(pydantic.BaseModel):
    Weight: float | None = None
    State: str  # TODO: enum
    Terms: Any = None  # list[dict[str, TermDefinition]] = None
    Definition: EntityDefinition | None = None
    Binding: Any = None
    SemanticType: str | None = None
    Visibility: Any = None
    Hidden: bool = False
    NameType: Any = None
    Units: list[str] = []

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )


class RelationshipBinding(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    ConceptualEntity: str


class PhrasingAttributeRole(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    Role: str


# TODO: Subtype
class PhrasingAttribute(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        # extra="forbid",  # TODO: undo comment
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    Adjective: PhrasingAttributeRole | None = None
    Measurement: PhrasingAttributeRole | None = None
    Object: PhrasingAttributeRole | None = None
    Subject: PhrasingAttributeRole | None = None

    Adjectives: list[Any] = []
    Antonyms: list[Any] = []
    Prepositions: list[Any] = []
    Verbs: list[Any] = []


class RelationshipPhrasing(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    Name: PhrasingAttribute | None = None
    Attribute: PhrasingAttribute | None = None
    Verb: PhrasingAttribute | None = None
    Adjective: PhrasingAttribute | None = None
    Preposition: PhrasingAttribute | None = None
    DynamicAdjective: PhrasingAttribute | None = None
    State: str | None = None  # TODO: enum
    Weight: float | None = None


class RelationshipRoleEntity(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    Entity: str


class RelationshipRole(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    Target: RelationshipRoleEntity


class LinguisticMetadataRelationship(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    Binding: RelationshipBinding
    Phrasings: list[RelationshipPhrasing] = []
    Roles: dict[str, RelationshipRole | Any]
    State: str | None = None
    SemanticSlots: Any = None
    Conditions: Any = None


class LinguisticMetadataContent(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        use_enum_values=False,
        json_schema_mode_override="serialization",
        validate_assignment=True,
        protected_namespaces=(),
    )
    Version: SemanticVersion
    Language: str
    DynamicImprovement: str | None = None
    Relationships: dict[str, LinguisticMetadataRelationship] | None = None
    Entities: dict[str, LinguisticMetadataEntity] | None = None
    Examples: list[dict[str, dict[str, str]]] | None = None


class LinguisticMetadata(SsasBaseTable):
    content: pydantic.Json[LinguisticMetadataContent]
    content_type: int
    culture_id: int

    modified_time: datetime.datetime

    def culture(self) -> "Culture":
        return self.tabular_model.cultures.find({"id": self.culture_id})

    def pbi_core_name(self) -> str:
        return self.culture().pbi_core_name()

    @classmethod
    def _db_command_obj_name(cls) -> str:
        return "LinguisticMetadata"

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        return LineageNode(self, lineage_type, [self.culture().get_lineage(lineage_type)])
