from pbi_core import LocalReport


def test_measure_set_name():
    ssas_pbix = LocalReport.load_pbix("example_pbis/test_ssas.pbix")
    viz = ssas_pbix.static_files.layout.sections[0].visualContainers[1]

    old_data = []
    if ret := viz.get_data(ssas_pbix.ssas):
        old_data = ret.data

    c = ssas_pbix.ssas.measures.find({"name": "Measure 3"})
    c.set_name("Measure 32", ssas_pbix.static_files.layout)

    new_data = []
    if ret := viz.get_data(ssas_pbix.ssas):
        new_data = ret.data
    assert len(old_data) == len(new_data)
    old_keys = set(old_data[0].keys())
    new_keys = set(new_data[0].keys())
    print(old_keys, new_keys)
    assert len(old_keys - new_keys) == 1
    assert len(new_keys - old_keys) == 1
    assert (old_keys - new_keys) == {"[Measure_3]"}
    assert (new_keys - old_keys) == {"[Measure_32]"}

    for o, n in zip(old_data, new_data, strict=True):
        print(o, n)
        for c in old_keys & new_keys:
            assert o[c] == n[c]
        assert o["[Measure_3]"] == n["[Measure_32]"]
