from pbi_core import LocalReport, report
from pbi_core.ssas.model_tables import column
from pbi_core.ssas.model_tables.column.enums import DataCategory

def test_table_alteration():
    report = LocalReport.load_pbix("test.pbix")
    table = report.ssas.tables.find({"name": "Table"})

    table.is_hidden = True
    table.alter()

    report.save_pbix("test_out.pbix")

def test_table_data(ssas_pbix):
    table = ssas_pbix.ssas.tables.find({"name": "Table"})
    data = table.data(head=10)
    assert len(data) == 10


def test_table_column(ssas_pbix):
    table = ssas_pbix.ssas.tables.find({"name": "Table"})
    columns = table.columns()
    # TODO: why is Value non-normal?
    assert {col.name() for col in columns} == {"Value", "RowNumber-2662979B-1795-4F74-8F37-6A1BA8059B61"}


def test_table_parents(ssas_pbix):
    table = ssas_pbix.ssas.tables.find({"name": "Table"})
    parents = table.parents()
    assert len(parents) == 1
    assert {p.pbi_core_name() for p in parents} == {"Model"}


def test_table_children(ssas_pbix):
    table = ssas_pbix.ssas.tables.find({"name": "Table"})
    children = table.children()
    print({c.pbi_core_name() for c in children})
    assert len(children) == 9
    assert {c.pbi_core_name() for c in children} == {'Table', 'RowNumber-2662979B-1795-4F74-8F37-6A1BA8059B61', 'Value', 'PBI_Id', 'SummarizationSetBy', 'Measure 4', 'complicated_measure'}
    assert {c.__class__.__name__ for c in children} == {'Measure', 'Column', 'AttributeHierarchy', 'Partition', 'Annotation'}
