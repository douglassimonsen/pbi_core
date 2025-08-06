class RuleGroup:
    name: str
    rules: list["BaseRule"]


class RuleResult:
    rule: type["BaseRule"]
    message: str
    trace: tuple[str | int, ...] | None

    def __init__(self, rule: type["BaseRule"], message: str, trace: tuple[str | int, ...] | None = None) -> None:
        self.rule = rule
        self.message = message
        self.trace = trace


class BaseRule:
    name: str
    description: str

    @classmethod
    def check(cls) -> list["RuleResult"]:
        """Check if the rule is violated.

        This method should be overridden in subclasses.
        """
        msg = "This method should be overridden in subclasses."
        raise NotImplementedError(msg)
