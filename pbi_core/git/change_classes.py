from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .to_markdown import to_markdown


class ChangeType(Enum):
    ADDED = "ADDED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"


@dataclass
class Change:
    id: str
    change_type: ChangeType


@dataclass
class FilterChange:
    pass


@dataclass
class LayoutChange(Change):
    filters: list[FilterChange] = field(default_factory=list)


@dataclass
class SectionChange(Change):
    filters: list[FilterChange] = field(default_factory=list)


@dataclass
class VisualChange(Change):
    filters: list[FilterChange] = field(default_factory=list)


@dataclass
class SsasChange(Change):
    entity_type: str  # e.g., "table", "measure", "column"
    entity: Any  # The entity itself, e.g., a table or measure object
    field_changes: dict[str, tuple[Any, Any]] = field(default_factory=dict)  # field name to [old_value, new_value]


@dataclass
class DiffReport:
    layout_changes: list[LayoutChange]
    section_changes: list[SectionChange]
    visual_changes: list[VisualChange]
    ssas_changes: dict[str, list[SsasChange]]

    def to_markdown(self) -> str:
        """Convert the diff report to a markdown string."""
        return to_markdown(self)
