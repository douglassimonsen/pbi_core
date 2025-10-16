from pbi_core import LocalReport


def test_performance_analysis():
    report = LocalReport.load_pbix("example_section_visibility.pbix")
    perf = report.static_files.layout.sections[0].get_performance(report.ssas)
    assert perf