from pbi_core import LocalReport
from pbi_core.ssas.model_tables.column.enums import DataCategory

def test_column_alteration():
    report = LocalReport.load_pbix("test.pbix")
    column = report.ssas.columns.find({"name": "Value"})

    column.data_category = DataCategory.POSTAL_CODE
    column.format_string = "#,0"
    column.alter()

    report.save_pbix("test_out.pbix")

def test_column_data():
    report = LocalReport.load_pbix("test.pbix")
    column = report.ssas.columns.find({"name": "Value"})
    data = column.data(head=10)
    assert len(data) == 10
