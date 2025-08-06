from pbi_parsers import dax

from pbi_core.ruff.base_rule import BaseRule, RuleResult
from pbi_core.ssas.model_tables.measure import Measure


class CapitalizeFunctionNames(BaseRule):
    id = "DAX-007"
    name = "Capitalize Function Names"
    description = """
        Function names in DAX expressions should be capitalized.
        This helps maintain consistency and readability in DAX expressions.
    """

    @classmethod
    def check(cls, measure: Measure) -> list[RuleResult]:
        if not isinstance(measure.expression, str):
            return []
        ast = dax.to_ast(measure.expression)
        if ast is None:
            return []

        ret = []
        for function in dax.utils.find_all(ast, dax.exprs.FunctionExpression):
            if not function.function_name().isupper():
                message = f"Function '{function.function_name()}' should be capitalized."
                ret.append(
                    RuleResult(
                        rule=cls,
                        message=message,
                        context=dax.utils.highlight_section(function),
                        trace=("measure", measure.table().name, measure.name, "expression"),
                    ),
                )
        return ret
