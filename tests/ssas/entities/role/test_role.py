

from pbi_core import LocalReport


def test_role_children(ssas_pbix):
    expr = ssas_pbix.ssas.roles.find(2941)
    children = expr.children()
    assert len(children) == 2
    assert {c.pbi_core_name() for c in children} == {'main_table', 'PBI_Id'}
    assert {c.__class__.__name__ for c in children} == {'TablePermission', 'Annotation'}
    
def test_role_parents(ssas_pbix):
    expr = ssas_pbix.ssas.roles.find(2941)
    parents = expr.parents()
    assert len(parents) == 1
    assert {p.pbi_core_name() for p in parents} == {'Model'}
    assert {p.__class__.__name__ for p in parents} == {'Model'}

def test_role_alter():
    ssas_pbix = LocalReport.load_pbix("test_ssas.pbix")
    expr = ssas_pbix.ssas.roles.find(2941)
    expr.description = "test description"
    expr.alter()

def test_role_delete():
    ssas_pbix = LocalReport.load_pbix("test_ssas.pbix")
    expr = ssas_pbix.ssas.roles.find(2941)
    expr.delete()

