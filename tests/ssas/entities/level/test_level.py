def test_level_children(ssas_pbix):
    expr = ssas_pbix.ssas.levels.find(1660)
    children = expr.children()
    assert len(children) == 0


def test_level_parents(ssas_pbix):
    expr = ssas_pbix.ssas.levels.find(1660)
    parents = expr.parents()
    assert len(parents) == 5
    assert {p.pbi_core_name() for p in parents} == {
        "LocalDateTable_f1dd39f2-2d79-466b-a0dd-7ac4c0d918ee",
        "Date Hierarchy",
        "Day",
        "Model",
        "Date",
    }
    assert {p.__class__.__name__ for p in parents} == {"Column", "Hierarchy", "Table", "Model"}


def test_level_alter(ssas_pbix):
    expr = ssas_pbix.ssas.levels.find(1660)
    expr.description = "test description"
    expr.alter()


def test_level_delete(ssas_pbix):
    expr = ssas_pbix.ssas.levels.find(1660)
    expr.delete()
