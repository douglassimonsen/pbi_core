from pbi_core import LocalReport

from .layout.section import visual_alignment
from .layout.theme import theme_colors


def check_rules(report: LocalReport) -> None:
    """Run all rules on the report."""
    # Run theme colors rule
    for section in report.static_files.layout.sections:
        visual_alignment.VisualXAlignment.check(section)
    theme_colors.ThemeColorsProtanopia.check(report.static_files.themes)

    # Add more rules as needed
    # e.g., ConsistentFontRule.check(report.static_files.layout)
    # e.g., ColorContrastRule.check(report.static_files.layout)
    # e.g., LayoutConsistencyRule.check(report.static_files.layout)
    # e.g., PerformanceRule.check(report.ssas, report.static_files.layout)
