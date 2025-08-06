import json
from typing import TYPE_CHECKING
from zipfile import ZipFile

from .layout import Layout

if TYPE_CHECKING:
    from _typeshed import StrPath

LAYOUT_ENCODING = "utf-16-le"


def load_pbix(path: "StrPath") -> Layout:
    zipfile = ZipFile(path, mode="r")
    layout_json = json.loads(zipfile.read("Report/Layout").decode(LAYOUT_ENCODING))
    ret: Layout = Layout.model_validate(layout_json)
    return ret
