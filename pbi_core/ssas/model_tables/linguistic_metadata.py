import datetime
from enum import IntEnum
from typing import TYPE_CHECKING

import pydantic
from pydantic_extra_types.semantic_version import SemanticVersion

from pbi_core.lineage import LineageNode, LineageType
from pbi_core.pydantic import BaseValidation
from pbi_core.ssas.server.tabular_model import SsasEditableRecord

if TYPE_CHECKING:
    from .culture import Culture


class ContentType(IntEnum):
    Xml = 0
    Json = 1


class EntityDefinitionBinding(BaseValidation):
    ConceptualEntity: str
    ConceptualProperty: str | None = None
    VariationSource: str | None = None
    VariationSet: str | None = None
    Hierarchy: str | None = None
    HierarchyLevel: str | None = None


class EntityDefinition(BaseValidation):
    Binding: EntityDefinitionBinding


class TermSourceType(IntEnum):
    pass


class TermSource(BaseValidation):
    Type: TermSourceType | None = None
    Agent: str


class TermDefinitionState(IntEnum):
    pass


class TermDefinitionType(IntEnum):
    pass


class TermDefinition(BaseValidation):
    State: TermDefinitionState
    Source: TermSource
    Weight: float
    Type: TermDefinitionType | None = None


class LinguisticMetadataState(IntEnum):
    pass


class LinguisticMetadataEntity(BaseValidation):
    Weight: float | None = None
    State: LinguisticMetadataState
    Terms: list[dict[str, TermDefinition]] | None = None
    Definition: EntityDefinition | None = None
    Binding: EntityDefinitionBinding | None = None
    SemanticType: str | None = None
    Visibility: int = None
    Hidden: bool = False
    NameType: int = None
    Units: list[str] = []


class RelationshipBinding(BaseValidation):
    ConceptualEntity: str


class PhrasingAttributeRole(BaseValidation):
    Role: str


# TODO: Subtype
class PhrasingAttribute(BaseValidation):
    model_config = pydantic.ConfigDict(
        extra="forbid",
    )
    Adjective: PhrasingAttributeRole | None = None
    Measurement: PhrasingAttributeRole | None = None
    Object: PhrasingAttributeRole | None = None
    Subject: PhrasingAttributeRole | None = None

    Adjectives: list[int] = []
    Antonyms: list[int] = []
    Prepositions: list[int] = []
    Verbs: list[int] = []


class RelationshipPhrasingState(IntEnum):
    pass


class RelationshipPhrasing(BaseValidation):
    Name: PhrasingAttribute | None = None
    Attribute: PhrasingAttribute | None = None
    Verb: PhrasingAttribute | None = None
    Adjective: PhrasingAttribute | None = None
    Preposition: PhrasingAttribute | None = None
    DynamicAdjective: PhrasingAttribute | None = None
    State: RelationshipPhrasingState | None = None
    Weight: float | None = None


class RelationshipRoleEntity(BaseValidation):
    Entity: str


class RelationshipRole(BaseValidation):
    Target: RelationshipRoleEntity


class LinguisticMetadataRelationship(BaseValidation):
    Binding: RelationshipBinding
    Phrasings: list[RelationshipPhrasing] = []
    Roles: dict[str, RelationshipRole | int]
    State: str | None = None
    SemanticSlots: int = None
    Conditions: int = None


class LinguisticMetadataContent(BaseValidation):
    Version: SemanticVersion
    Language: str
    DynamicImprovement: str | None = None
    Relationships: dict[str, LinguisticMetadataRelationship] | None = None
    Entities: dict[str, LinguisticMetadataEntity] | None = None
    Examples: list[dict[str, dict[str, str]]] | None = None


class LinguisticMetadata(SsasEditableRecord):
    """TBD.

    SSAS spec: https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/f8924a45-70da-496a-947a-84b8d5beaae6
    """

    content: pydantic.Json[LinguisticMetadataContent]
    content_type: ContentType
    culture_id: int

    modified_time: datetime.datetime

    def culture(self) -> "Culture":
        return self.tabular_model.cultures.find({"id": self.culture_id})

    def pbi_core_name(self) -> str:
        """Returns the name displayed in the PBIX report."""
        return self.culture().pbi_core_name()

    @classmethod
    def _db_command_obj_name(cls) -> str:
        return "LinguisticMetadata"

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        if lineage_type == "children":
            return LineageNode(self, lineage_type)
        return LineageNode(self, lineage_type, [self.culture().get_lineage(lineage_type)])
