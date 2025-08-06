from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ChangeType(Enum):
    ADDED = 1
    UPDATED = 2
    DELETED = 3


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
    field_changes: dict[str, tuple[Any, Any]] = field(default_factory=dict)  # field name to [old_value, new_value]


@dataclass
class DiffReport:
    layout_changes: list[LayoutChange]
    section_changes: list[LayoutChange]
    visual_changes: list[VisualChange]
    ssas_changes: dict[str, list[SsasChange]]
