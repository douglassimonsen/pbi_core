import json
from typing import TYPE_CHECKING
from zipfile import ZipFile

from .layout.layout import Layout

if TYPE_CHECKING:
    from _typeshed import StrPath

LAYOUT_ENCODING = "utf-16-le"


class StaticElements:
    layout: Layout

    def __init__(self, path: "StrPath"):
        zipfile = ZipFile(path, mode="r")

        layout_json = json.loads(zipfile.read("Report/Layout").decode(LAYOUT_ENCODING))
        self.layout = Layout.model_validate(layout_json)
