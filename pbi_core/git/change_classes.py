from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ChangeType(Enum):
    ADDED = "ADDED"
    UPDATED = "UPDATED"
    DELETED = "DELETED"
    NO_CHANGE = "NO_CHANGE"  # used when only changes in children are present


@dataclass
class Change:
    id: str
    change_type: ChangeType


@dataclass
class FilterChange(Change):
    entity: Any
    field_changes: dict[str, tuple[Any, Any]] = field(default_factory=dict)  # field name to [old_value, new_value]


@dataclass
class VisualChange(Change):
    entity: Any
    filters: list[FilterChange] = field(default_factory=list)
    field_changes: dict[str, tuple[Any, Any]] = field(default_factory=dict)  # field name to [old_value, new_value]

    def to_markdown(self) -> str:
        """Convert the visual change to a markdown string."""
        if self.change_type == ChangeType.NO_CHANGE:
            return ""
        if self.change_type in (ChangeType.ADDED, ChangeType.DELETED):
            return ""
        return ""


@dataclass
class SectionChange(Change):
    entity: Any
    filters: list[FilterChange] = field(default_factory=list)
    field_changes: dict[str, tuple[Any, Any]] = field(default_factory=dict)  # field name to [old_value, new_value]
    visuals: list[VisualChange] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Convert the section change to a markdown string."""
        if self.change_type == ChangeType.NO_CHANGE:
            return ""
        if self.change_type in (ChangeType.ADDED, ChangeType.DELETED):
            return ""
        return ""


@dataclass
class LayoutChange(Change):
    entity: Any
    filters: list[FilterChange] = field(default_factory=list)
    field_changes: dict[str, tuple[Any, Any]] = field(default_factory=dict)  # field name to [old_value, new_value]
    sections: list[SectionChange] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Convert the layout change to a markdown string."""
        if self.change_type == ChangeType.NO_CHANGE:
            return ""
        if self.change_type in (ChangeType.ADDED, ChangeType.DELETED):
            return ""
        return """

"""


@dataclass
class SsasChange(Change):
    entity_type: str  # e.g., "table", "measure", "column"
    entity: Any  # The entity itself, e.g., a table or measure object
    field_changes: dict[str, tuple[Any, Any]] = field(default_factory=dict)  # field name to [old_value, new_value]


@dataclass
class DiffReport:
    layout_changes: LayoutChange
    ssas_changes: dict[str, list[SsasChange]]

    def to_markdown(self) -> str:
        """Convert the diff report to a markdown string."""
        from .to_markdown import to_markdown

        return to_markdown(self)

    def layout_updates(self) -> int:
        """Count the number of layout updates."""
        return len(self.layout_changes.field_changes) + len(self.layout_changes.filters)

    def section_updates(self) -> int:
        """Count the number of section updates."""
        return sum(len(section.field_changes) + len(section.filters) for section in self.layout_changes.sections)

    def visual_updates(self) -> int:
        """Count the number of visual updates."""
        return sum(
            len(visual.field_changes) + len(visual.filters)
            for section in self.layout_changes.sections
            for visual in section.visuals
        )
