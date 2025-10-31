from pbi_core import LocalReport


def test_format_string_definition_children(ssas_pbix):
    expr = ssas_pbix.ssas.format_string_definitions.find(2802)
    children = expr.children()
    assert len(children) == 0


def test_format_string_definition_parents(ssas_pbix: LocalReport):
    expr = ssas_pbix.ssas.format_string_definitions.find(2802)
    parents = expr.parents()
    assert len(parents) == 4
    assert {p.pbi_core_name() for p in parents} == {"Measure", "a", "main_table", "Model"}
    assert {p.__class__.__name__ for p in parents} == {"Measure", "Column", "Table", "Model"}


def test_format_string_definition_alter(ssas_pbix):
    expr = ssas_pbix.ssas.format_string_definitions.find(2802)
    expr.expression = 'FORMAT([SalesAmount], "Currency")'
    expr.alter()


def test_format_string_definition_delete():
    ssas_pbix = LocalReport.load_pbix("test_ssas.pbix")
    expr = ssas_pbix.ssas.format_string_definitions.find(2802)
    expr.delete()
