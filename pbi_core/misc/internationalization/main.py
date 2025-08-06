from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...static_files import Layout, Section

if TYPE_CHECKING:
    from _typeshed import StrPath


@dataclass
class StaticElement:
    xpath: list[str | int]
    field: str
    text: str


class StaticElements:
    static_elements: dict[str, list[StaticElement]] = {}

    def __init__(self) -> None:
        pass

    def to_csv(self) -> None:
        pass

    def to_excel(self, path: "StrPath") -> None:
        import json

        import openpyxl

        wb = openpyxl.Workbook()
        for object_type, objects in self.static_elements.items():
            ws = wb.create_sheet(object_type)
            for j, name in enumerate(["xpath", "field", "default"]):
                ws.cell(1, j + 1).value = name
            for i, object in enumerate(objects):
                ws.cell(2 + i, 1).value = json.dumps(object.xpath)
                ws.cell(2 + i, 2).value = object.field
                ws.cell(2 + i, 3).value = object.text
        wb.remove(wb["Sheet"])
        wb.save(path)


def get_static_elements(layout: Layout) -> StaticElements:
    ret = StaticElements()
    for section in layout.find_all(Section):
        ret.static_elements.setdefault("section", []).append(
            StaticElement(
                xpath=section._xpath,
                field="displayName",
                text=section.displayName,
            )
        )
    return ret
