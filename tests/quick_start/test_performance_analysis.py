from pbi_core import LocalReport


def test_performance_analysis():
    report = LocalReport.load_pbix("test.pbix")
    section = report.static_files.layout.sections[0]
    print(section)
    perf = section.get_performance(report.ssas)
    assert perf
