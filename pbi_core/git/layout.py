from typing import TYPE_CHECKING

from .change_classes import ChangeType, LayoutChange, SectionChange, VisualChange

if TYPE_CHECKING:
    from pbi_core.static_files.layout.layout import Layout, Section


def section_diff(parent_section: "Section", child_section: "Section") -> tuple[list[SectionChange], list[VisualChange]]:
    section_changes: list[SectionChange] = []
    visual_changes: list[VisualChange] = []

    parent_visuals = {visual.pbi_core_id(): visual for visual in parent_section.visualContainers}
    child_visuals = {visual.pbi_core_id(): visual for visual in child_section.visualContainers}

    visual_changes.extend(
        VisualChange(visual_id, ChangeType.DELETED)
        for visual_id in set(parent_visuals.keys()) - set(child_visuals.keys())
    )
    visual_changes.extend(
        VisualChange(visual_id, ChangeType.ADDED)
        for visual_id in set(child_visuals.keys()) - set(parent_visuals.keys())
    )
    for visual_id in set(parent_visuals.keys()) & set(child_visuals.keys()):
        parent_visual = parent_visuals[visual_id]
        child_visual = child_visuals[visual_id]

    return section_changes, visual_changes


def layout_diff(
    parent: "Layout",
    child: "Layout",
) -> tuple[list[LayoutChange], list[SectionChange], list[VisualChange]]:
    layout_changes: list[LayoutChange] = []
    section_changes: list[SectionChange] = []
    visual_changes: list[VisualChange] = []

    parent_sections = {x.name: x for x in parent.sections}
    child_sections = {x.name: x for x in child.sections}
    for section_name in set(parent_sections.keys()) - set(child_sections.keys()):
        section_changes = [
            SectionChange(
                section_name,
                ChangeType.DELETED,
            ),
        ]
        visual_changes.extend(
            VisualChange(visual.pbi_core_id(), ChangeType.DELETED)
            for visual in parent_sections[section_name].visualContainers
        )

    for section_name in set(child_sections.keys()) - set(parent_sections.keys()):
        section_changes = [
            SectionChange(
                section_name,
                ChangeType.ADDED,
            ),
        ]
        visual_changes.extend(
            VisualChange(visual.pbi_core_id(), ChangeType.ADDED) for visual in child_sections[section_name].visualContainers
        )

    for section_name in set(parent_sections.keys()) & set(child_sections.keys()):
        parent_section = parent_sections[section_name]
        child_section = child_sections[section_name]
        sub_section_changes, sub_visual_changes = section_diff(parent_section, child_section)
        section_changes.extend(sub_section_changes)
        visual_changes.extend(sub_visual_changes)

    return layout_changes, section_changes, visual_changes
