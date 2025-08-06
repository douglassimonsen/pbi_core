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
    id: str
    name: str
    description: str
