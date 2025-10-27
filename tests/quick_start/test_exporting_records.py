from pbi_core import LocalReport


def test_exporting_records(ssas_pbix):
    values = ssas_pbix.ssas.columns.find({"explicit_name": "a"}).data()
    assert values
    values2 = ssas_pbix.ssas.tables.find({"name": "Table"}).data()
    assert values2

    measure = ssas_pbix.ssas.measures.find({"name": "Measure"})
    # Note: the first column is a hidden row-count column that can't be used in measures
    column = [x for x in measure.table().columns() if not x.is_key][0]
    values3 = measure.data(column, head=10)
    assert values3