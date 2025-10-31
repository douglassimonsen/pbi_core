from pbi_core import LocalReport


def test_partition_children(ssas_pbix):
    expr = ssas_pbix.ssas.partitions.find(618)
    children = expr.children()
    assert len(children) == 0


def test_partition_parents(ssas_pbix):
    expr = ssas_pbix.ssas.partitions.find(618)
    parents = expr.parents()
    assert len(parents) == 2
    assert {p.pbi_core_name() for p in parents} == {"Model", "Query1"}
    assert {p.__class__.__name__ for p in parents} == {"Model", "Table"}


def test_partition_alter(ssas_pbix):
    expr = ssas_pbix.ssas.partitions.find(618)
    expr.description = "test description"
    expr.alter()


def test_partition_delete():
    ssas_pbix = LocalReport.load_pbix("test_ssas.pbix")
    expr = ssas_pbix.ssas.partitions.find(618)
    expr.delete()
