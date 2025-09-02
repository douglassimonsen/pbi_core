from pbi_core.logging import get_logger
from pbi_core.report.local.main import LocalReport

from .get_static_elements import get_static_elements
from .text_elements import TextElements

logger = get_logger()


def get_source_text_elements(report: LocalReport) -> TextElements:
    static_elements = get_static_elements(report.static_files.layout)
    # ssas_elements = get_ssas_elements(report.ssas)
    return TextElements(text_elements=static_elements.text_elements)
