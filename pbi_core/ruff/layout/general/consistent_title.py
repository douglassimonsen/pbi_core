from ...base_rule import BaseRule, RuleResult


class ConsistentTitle(BaseRule):
    id = "GEN-002"
    name = "Consistent Title"
    description = """
        All Sections should have a title in the top left quadrant of the report.
        A title should be a text box visual.
    """

    @classmethod
    def check(cls, layout) -> list[RuleResult]:
        return []
