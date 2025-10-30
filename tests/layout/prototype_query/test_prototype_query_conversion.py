from pbi_core import LocalReport
from pbi_core.static_files.layout.visual_container import VisualContainer


def test_prototype_query_conversion():
    ssas_report = LocalReport.load_pbix("test_ssas.pbix")
    cmd = ssas_report.static_files.layout.find(VisualContainer)._get_data_command()
    assert cmd is not None
    query = "".join(cmd.get_dax(ssas_report.ssas).dax.split())
    expected = "".join(["DEFINE", "VAR", "__DS0Core", "=", "SUMMARIZECOLUMNS(", "'main_table'[a],", "'main_table'[b],", '"Sumb",', "CALCULATE(SUM('main_table'[b])),", '"Suma",', "CALCULATE(SUM('main_table'[a]))", ")", "EVALUATE", "__DS0Core", "ORDER", "BY", "[Sumb]", "DESC"])
    assert query.strip() == expected
