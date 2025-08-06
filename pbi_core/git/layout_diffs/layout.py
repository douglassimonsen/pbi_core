from typing import TYPE_CHECKING

from pbi_core.git.change_classes import ChangeType, LayoutChange, SectionChange, VisualChange

from .filters import filter_diff
from .section import section_diff

if TYPE_CHECKING:
    from pbi_core.static_files.layout.layout import Layout


def layout_diff_update(parent: "Layout", child: "Layout") -> LayoutChange | None:
    field_changes = {}
    for field in []:  # no simple fields to compare in Layout
        parent_val = getattr(parent, field, None)
        child_val = getattr(child, field, None)
        if parent_val != child_val and not (parent_val is None and child_val is None):
            field_changes[field] = (parent_val, child_val)
    filter_changes = filter_diff(parent.filters, child.filters)  # type: ignore reportArgumentType

    if field_changes:
        return LayoutChange(
            id="layout",
            change_type=ChangeType.UPDATED,
            entity=parent,
            field_changes=field_changes,
            filters=filter_changes,
        )
    return None


def layout_diff(
    parent: "Layout",
    child: "Layout",
) -> tuple[LayoutChange | None, list[SectionChange], list[VisualChange]]:
    section_changes: list[SectionChange] = []
    visual_changes: list[VisualChange] = []

    parent_sections = {x.name: x for x in parent.sections}
    child_sections = {x.name: x for x in child.sections}
    for section_name in set(parent_sections.keys()) - set(child_sections.keys()):
        section_changes = [
            SectionChange(
                id=section_name,
                change_type=ChangeType.DELETED,
                entity=parent_sections[section_name],
            ),
        ]
        visual_changes.extend(
            VisualChange(visual.pbi_core_id(), ChangeType.DELETED, visual)
            for visual in parent_sections[section_name].visualContainers
        )

    for section_name in set(child_sections.keys()) - set(parent_sections.keys()):
        section_changes = [
            SectionChange(
                id=section_name,
                change_type=ChangeType.ADDED,
                entity=child_sections[section_name],
            ),
        ]
        visual_changes.extend(
            VisualChange(visual.pbi_core_id(), ChangeType.ADDED, visual)
            for visual in child_sections[section_name].visualContainers
        )

    for section_name in set(parent_sections.keys()) & set(child_sections.keys()):
        parent_section = parent_sections[section_name]
        child_section = child_sections[section_name]
        sub_section_changes, sub_visual_changes = section_diff(parent_section, child_section)
        if sub_section_changes:
            section_changes.append(sub_section_changes)
        visual_changes.extend(sub_visual_changes)

    layout_changes = layout_diff_update(parent, child)
    return layout_changes, section_changes, visual_changes
