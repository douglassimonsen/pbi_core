from ....static_files.layout.layout import Layout
from ....static_files.layout.visual_container import VisualContainer
from ....static_files.layout.visuals.properties.base import LiteralExpression
from ...base_rule import BaseRule, RuleResult
from ...utils.main import get_config_values

MAX_FONTS = 2


def get_fonts(layout: Layout) -> set[str]:
    fonts: set[str] = set()

    for visual in layout.find_all(VisualContainer):
        if visual.config.singleVisual is None:
            continue
        sv = visual.config.singleVisual
        vc_config_values = get_config_values(sv.vcObjects)
        config_values = get_config_values(sv.objects)
        for (_, field), value in vc_config_values.items():
            if field == "fontFamily" and isinstance(value, LiteralExpression):
                fonts.add(str(value.expr.value()))
        for (_, field), value in config_values.items():
            if field == "fontFamily" and isinstance(value, LiteralExpression):
                fonts.add(str(value.expr.value()))
    return fonts


class ConsistentFont(BaseRule):
    id = "GEN-001"
    name = "Consistent Font"
    description = "No more than 2 fonts should be used in a report"

    @classmethod
    def check(cls, layout: Layout) -> list[RuleResult]:
        fonts = get_fonts(layout)
        if len(fonts) > MAX_FONTS:
            return [
                RuleResult(
                    rule=cls,
                    message=f"Found {len(fonts)} different fonts: {', '.join(sorted(fonts))}. "
                    "Consider using no more than 2 fonts for consistency.",
                ),
            ]
        return []
