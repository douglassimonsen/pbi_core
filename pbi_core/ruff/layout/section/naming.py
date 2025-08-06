from ....static_files.layout.section import Section
from ...base_rule import BaseRule, RuleResult

MAX_SECTION_NAME_LENGTH = 35


class ProperSectionName(BaseRule):
    id = "SEC-003"
    name = "Section Naming"
    description = """Section names should be human readable. This means no underscores, capital case usage, and less than 35 characters (the max Power BI allows before using ellipses)."""

    @classmethod
    def check(cls, section: Section) -> list[RuleResult]:
        section_name = section.name
        if "_" in section_name:
            return [
                RuleResult(
                    rule=cls,
                    trace=("section", section.name),
                    message=f"Section name '{section_name}' contains underscores. Consider using spaces instead.",
                ),
            ]
        if section_name != section_name.title():
            return [
                RuleResult(
                    rule=cls,
                    trace=("section", section.name),
                    message=f"Section name '{section_name}' is not in title case. "
                    "Consider capitalizing the first letter of each word.",
                ),
            ]
        if len(section_name) > MAX_SECTION_NAME_LENGTH:
            return [
                RuleResult(
                    rule=cls,
                    trace=("section", section.name),
                    message=f"Section name '{section_name}' is longer than 35 characters. Consider shortening it to improve readability.",
                ),
            ]
        return []
