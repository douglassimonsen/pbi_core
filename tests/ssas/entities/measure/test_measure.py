def test_measure_children(ssas_pbix):
    expr = ssas_pbix.ssas.measures.find(1595)
    children = expr.children()
    assert len(children) == 0


def test_measure_parents(ssas_pbix):
    expr = ssas_pbix.ssas.measures.find(1595)
    parents = expr.parents()
    assert len(parents) == 4
    assert {p.pbi_core_name() for p in parents} == {"main_table", "Model", "Query1", "a"}
    assert {p.__class__.__name__ for p in parents} == {"Table", "Model", "Column"}


def test_measure_alter(ssas_pbix):
    expr = ssas_pbix.ssas.measures.find(1595)
    expr.description = "1 + 2"
    expr.alter()


def test_measure_delete(ssas_pbix):
    expr = ssas_pbix.ssas.measures.find(1595)
    expr.delete()
