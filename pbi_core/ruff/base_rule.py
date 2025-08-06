from collections.abc import Iterable


class RuleGroup:
    name: str
    rules: Iterable[type["BaseRule"]]


class RuleResult:
    rule: type["BaseRule"]
    message: str
    context: str | None = None
    trace: tuple[str | int, ...] | None

    def __init__(
        self,
        rule: type["BaseRule"],
        message: str,
        context: str | None = None,
        trace: tuple[str | int, ...] | None = None,
    ) -> None:
        self.rule = rule
        self.message = message
        self.context = context
        self.trace = trace

    def __repr__(self) -> str:
        content = f"""{self.rule.id} - {self.rule.name}: {self.message}
-----
{self.context}
-----
Trace: {self.trace_string()}
"""
        return content

    def fix(self) -> None:
        """Attempt to fix the issue described by this rule result."""
        raise NotImplementedError("Subclasses may implement the fix method.")

    def trace_string(self) -> str:
        """Return a string representation of the trace."""
        if self.trace is None:
            return ""
        return ".".join(str(t) for t in self.trace)


class BaseRule:
    id: str
    name: str
    description: str

    @classmethod
    def check(cls, *args, **kwargs) -> list[RuleResult]:
        """Check the rule against the provided arguments and return a list of RuleResult."""
        raise NotImplementedError("Subclasses must implement the check method.")
