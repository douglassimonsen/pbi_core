def test_annotation_children(ssas_pbix):
    annotation = ssas_pbix.ssas.annotations.find(36)
    children = annotation.children()
    assert len(children) == 0


def test_annotation_parents(ssas_pbix):

    annotation = ssas_pbix.ssas.annotations.find(36)
    parents = annotation.parents()
    assert len(parents) == 3
    assert {p.pbi_core_name() for p in parents} == {'Model', 'DateTableTemplate_b1b26bde-e081-4a41-aa17-61487b3e6e3e', 'Date'}
    assert {p.__class__.__name__ for p in parents} == {'Model', 'Table', 'Column'}


def test_annotation_alter(ssas_pbix):
    annotation = ssas_pbix.ssas.annotations.find(36)
    annotation.value = "Updated Annotation Value"
    annotation.alter()


def test_annotation_delete(ssas_pbix):
    annotation = ssas_pbix.ssas.annotations.find(36)
    annotation.delete()