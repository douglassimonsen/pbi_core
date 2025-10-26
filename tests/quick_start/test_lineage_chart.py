from pbi_core import LocalReport


def test_lineage_chart():
    report = LocalReport.load_pbix("test.pbix")
    col = report.ssas.measures.find({"name": "Measure 4"})
    col.get_lineage("parents").to_mermaid()