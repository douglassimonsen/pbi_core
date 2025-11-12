import pytest

from pbi_core import LocalReport
from pbi_core.static_files.layout.visuals.action_button import ActionButton
from pbi_core.static_files.layout.visuals.base import BaseVisual, FilterSortOrder
from pbi_core.static_files.layout.visuals.generic import GenericVisual

ssas_pbix = LocalReport.load_pbix("example_pbis/test_ssas.pbix")


@pytest.mark.parametrize(
    ("cls", "filter_func", "cnt"),
    [
        (BaseVisual, None, 11),
        (ActionButton, None, 7),
        (BaseVisual, lambda b: b.filterSortOrder == FilterSortOrder.NA, 11),
        ((ActionButton, GenericVisual), None, 11),
        (BaseVisual, {"filterSortOrder": FilterSortOrder.NA}, 11),
    ],
)
def test_find_all(cls, filter_func, cnt):
    vizes = ssas_pbix.static_files.layout.find_all(cls, filter_func)
    assert len(vizes) == cnt


def test_find_all_section():
    vizes = ssas_pbix.static_files.layout.sections[0].find_all(BaseVisual)
    assert len(vizes) == 4
