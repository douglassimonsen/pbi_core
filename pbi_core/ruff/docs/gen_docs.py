import pathlib

import jinja2

from pbi_core.ruff.dax import DaxFormattingRules, DaxPerformanceRules
from pbi_core.ruff.layout import LayoutRules, SectionRules, ThemeRules, VisualRules

templates = {
    x.stem: jinja2.Template(x.read_text())
    for x in (pathlib.Path(__file__).parent / "templates").iterdir()
    if x.suffix == ".md"
}
group_info = []
for group in [DaxFormattingRules, DaxPerformanceRules, LayoutRules, SectionRules, ThemeRules, VisualRules]:
    group_info.append({
        "name": group.name,
        "rules": len(group.rules),
    })
    with (
        pathlib.Path(__file__).parents[3] / "docs/docs/ruff/rule_groups/" / f"{group.name.replace(' ', '_')}.md"
    ).open("w", encoding="utf-8") as f:
        f.write(templates["group"].render(group=group))

with (pathlib.Path(__file__).parents[3] / "docs/docs/ruff/main.md").open("w", encoding="utf-8") as f:
    f.write(templates["entry"].render(groups=group_info))
