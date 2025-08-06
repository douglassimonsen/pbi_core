from typing import TYPE_CHECKING

from pbi_core.git.change_classes import ChangeType, SectionChange, VisualChange

from .filters import filter_diff
from .visual import visual_diff

if TYPE_CHECKING:
    from pbi_core.static_files.layout.layout import Section


def section_diff(
    parent_section: "Section",
    child_section: "Section",
) -> tuple[SectionChange | None, list[VisualChange]]:
    visual_changes: list[VisualChange] = []

    parent_visuals = {visual.pbi_core_id(): visual for visual in parent_section.visualContainers}
    child_visuals = {visual.pbi_core_id(): visual for visual in child_section.visualContainers}

    visual_changes.extend(
        VisualChange(
            id=visual_id,
            change_type=ChangeType.DELETED,
            entity=parent_visuals[visual_id],
        )
        for visual_id in set(parent_visuals.keys()) - set(child_visuals.keys())
    )
    visual_changes.extend(
        VisualChange(
            id=visual_id,
            change_type=ChangeType.ADDED,
            entity=child_visuals[visual_id],
        )
        for visual_id in set(child_visuals.keys()) - set(parent_visuals.keys())
    )
    for visual_id in set(parent_visuals.keys()) & set(child_visuals.keys()):
        parent_visual = parent_visuals[visual_id]
        child_visual = child_visuals[visual_id]
        visual_object = visual_diff(parent_visual, child_visual)
        if visual_object:
            visual_changes.append(visual_object)

    field_changes = {}
    for field in ["name", "description"]:
        parent_val = getattr(parent_section, field, None)
        child_val = getattr(child_section, field, None)
        if parent_val != child_val and not (parent_val is None and child_val is None):
            field_changes[field] = (parent_val, child_val)

    section_changes = None
    if field_changes:
        section_changes = SectionChange(
            id=parent_section.name,
            change_type=ChangeType.UPDATED,
            entity=parent_section,
            filters=filter_diff(parent_section.filters, child_section.filters),  # type: ignore reportArgumentType
            field_changes=field_changes,
        )

    return section_changes, visual_changes
