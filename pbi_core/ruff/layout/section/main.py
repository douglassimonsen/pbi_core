from pbi_core.ruff.base_rule import RuleGroup, RuleResult
from pbi_core.static_files.layout.section import Section

from .visual_alignment import VisualXAlignment, VisualYAlignment


class SectionRules(RuleGroup):
    """Group of rules related to sections."""

    rules = [
        VisualXAlignment,
        VisualYAlignment,
    ]

    @classmethod
    def check(cls, section: Section) -> list[RuleResult]:
        results = []
        for rule in cls.rules:
            results.extend(rule.check(section))
        return results
