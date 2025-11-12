from pbi_core import LocalReport


def test_column_set_name():
    ssas_pbix = LocalReport.load_pbix("test_ssas.pbix")
    viz = ssas_pbix.static_files.layout.sections[0].visualContainers[0]

    old_data = []
    if ret := viz.get_data(ssas_pbix.ssas):
        old_data = ret.data

    c = ssas_pbix.ssas.columns.find({"name": "b"})
    c.set_name("b2", ssas_pbix.static_files.layout)

    new_data = []
    if ret := viz.get_data(ssas_pbix.ssas):
        new_data = ret.data
    assert len(old_data) == len(new_data)
    old_keys = set(old_data[0].keys())
    new_keys = set(new_data[0].keys())
    assert len(old_keys - new_keys) == 2
    assert len(new_keys - old_keys) == 2
    assert (old_keys - new_keys) == {"main_table[b]", "[Sumb]"}
    assert (new_keys - old_keys) == {"main_table[b2]", "[Sumb2]"}

    for o, n in zip(old_data, new_data, strict=True):
        print(o, n)
        for c in old_keys & new_keys:
            assert o[c] == n[c]
        assert o["main_table[b]"] == n["main_table[b2]"]
        assert o["[Sumb]"] == n["[Sumb2]"]
