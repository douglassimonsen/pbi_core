

def test_relationship_children(ssas_pbix):
    expr = ssas_pbix.ssas.relationships.find(1646)
    children = expr.children()
    assert len(children) == 1
    assert {c.pbi_core_name() for c in children} == {'Variation'}
    assert {c.__class__.__name__ for c in children} == {'Variation'}
    
def test_relationship_parents(ssas_pbix):
    expr = ssas_pbix.ssas.relationships.find(1646)
    parents = expr.parents()
    assert len(parents) == 6
    assert {p.pbi_core_name() for p in parents} == {'a', 'main_table', 'LocalDateTable_f1dd39f2-2d79-466b-a0dd-7ac4c0d918ee', 'Model', 'date_Column', 'Date'}
    assert {p.__class__.__name__ for p in parents} == {'Column', 'Table', 'Model'}

def test_relationship_alter(ssas_pbix):
    expr = ssas_pbix.ssas.relationships.find(1646)
    expr.name = "test name"
    expr.alter()

def test_relationship_delete(ssas_pbix):
    expr = ssas_pbix.ssas.relationships.find(1646)
    # TODO: cascade delete variations before enabling this
    # expr.delete()

