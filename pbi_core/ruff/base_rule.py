from collections.abc import Iterable
from typing import Any

from colorama import Fore, Style


class RuleGroup:
    name: str
    rules: Iterable[type["BaseRule"]]


class RuleResult:
    rule: type["BaseRule"]
    message: str
    context: str | None = None
    context_vars: dict[str, Any]
    trace: tuple[str | int, ...] | None

    def __init__(
        self,
        rule: type["BaseRule"],
        message: str,
        context: str | None = None,
        context_vars: dict[str, Any] | None = None,
        trace: tuple[str | int, ...] | None = None,
    ) -> None:
        self.rule = rule
        self.message = message
        self.context = context
        self.context_vars = context_vars or {}
        self.trace = trace

    def __repr__(self) -> str:
        context = ""
        if self.context:
            context = f"""-----
{self.context}
-----"""
        return f"""{Fore.RED}{self.rule.id}{Style.RESET_ALL} - {self.rule.name}: {self.message}
{context}
Trace: {self.trace_string()}
"""

    def fix(self) -> None:
        """Attempt to fix the issue described by this rule result."""
        msg = "Subclasses may implement the fix method."
        raise NotImplementedError(msg)

    def trace_string(self) -> str:
        """Return a string representation of the trace."""
        if self.trace is None:
            return ""
        return ".".join(str(t) for t in self.trace)

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the RuleResult."""
        return {
            "rule": self.rule.id,
            "message": self.message,
            "context": self.context,
            "context_vars": self.context_vars,
            "trace": self.trace_string(),
        }


class BaseRule:
    id: str
    name: str
    description: str

    @classmethod
    def check(cls, *args: Any, **kwargs: Any) -> list[RuleResult]:
        """Check the provided arguments and return a list of RuleResults."""
        msg = "Subclasses must implement the check method."
        raise NotImplementedError(msg)
