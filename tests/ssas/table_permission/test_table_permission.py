from pbi_core.ssas.model_tables.table_permission.enums import MetadataPermission


def test_table_permission_parents(ssas_pbix):
    tp = ssas_pbix.ssas.table_permissions.find(2942)
    parents = tp.parents()
    assert len(parents) == 3
    assert {p.pbi_core_name() for p in parents} == {"Model", "main_table", "test_role"}
    assert {p.__class__.__name__ for p in parents} == {"Model", "Table", "Role"}

def test_table_permission_children(ssas_pbix):
    tp = ssas_pbix.ssas.table_permissions.find(2942)
    children = tp.children()
    assert len(children) == 0 

def test_table_permission_alter(ssas_pbix):
    tp = ssas_pbix.ssas.table_permissions.find(2942)
    tp.metadata_permission = MetadataPermission.DEFAULT
    tp.filter_expression = "[a] > 5"
    tp.alter()

def test_table_permission_delete(ssas_pbix):
    tp = ssas_pbix.ssas.table_permissions.find(2942)
    tp.delete()