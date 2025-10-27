from pbi_core import LocalReport, report
from pbi_core.ssas.model_tables.column.enums import DataCategory

def test_column_alteration():
    report = LocalReport.load_pbix("test.pbix")
    column = report.ssas.columns.find({"name": "Value"})

    column.data_category = DataCategory.POSTAL_CODE
    column.format_string = "#,0"
    column.alter()

    report.save_pbix("test_out.pbix")

def test_column_data(ssas_pbix):
    column = ssas_pbix.ssas.columns.find({"name": "Value"})
    data = column.data(head=10)
    assert len(data) == 10


def test_column_table(ssas_pbix):
    column = ssas_pbix.ssas.columns.find({"name": "Value"})
    table = column.table()
    assert table.name == "Table"


def test_column_parents(ssas_pbix):
    column = ssas_pbix.ssas.columns.find({"name": "Value"})
    parents = column.parents()
    assert len(parents) == 1
    assert {p.pbi_core_name() for p in parents} == {"Table"}


def test_column_children(ssas_pbix):
    column = ssas_pbix.ssas.columns.find({"name": "Value"})
    children = column.children()
    assert len(children) == 3
    assert {c.pbi_core_name() for c in children} == {'Measure 4', 'Value', 'complicated_measure'}
    assert {c.__class__.__name__ for c in children} == {'Measure', 'AttributeHierarchy', 'Measure'}



