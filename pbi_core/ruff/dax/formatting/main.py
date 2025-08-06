from typing import TYPE_CHECKING

from ...base_rule import RuleGroup
from .camel_case_variable import CamelCaseMeasureName, CamelCaseVariable

if TYPE_CHECKING:
    from ....ssas.model_tables import Measure


class DaxFormattingRules(RuleGroup):
    """Group of rules related to DAX formatting."""

    name = "DAX Formatting Rules"
    rules = (
        CamelCaseMeasureName,
        CamelCaseVariable,
    )

    @classmethod
    def check(cls, measure: "Measure") -> list["RuleResult"]:
        """Check the measure for DAX formatting rules."""
        results = []
        for rule in cls.rules:
            results.extend(rule.check(measure))
        return results
