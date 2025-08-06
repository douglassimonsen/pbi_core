from pbi_core.ruff.base_rule import RuleGroup, RuleResult
from pbi_core.static_files.layout.section import Section

from .theme_colors import ThemeColors, ThemeColorsDeuteranopia, ThemeColorsProtanopia, ThemeColorsTritanopia


class ThemeRules(RuleGroup):
    """Group of rules related to theme colors."""

    name = "Theme Rules"
    rules = [
        ThemeColors,
        ThemeColorsProtanopia,
        ThemeColorsDeuteranopia,
        ThemeColorsTritanopia,
    ]

    @classmethod
    def check(cls, section: Section) -> list[RuleResult]:
        results = []
        for rule in cls.rules:
            results.extend(rule.check(section))
        return results
