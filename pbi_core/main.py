from typing import TYPE_CHECKING, Any, Optional

from .ssas.server import BaseTabularModel, LocalTabularModel, get_or_create_local_server
from .static_elements import StaticElements

if TYPE_CHECKING:
    from _typeshed import StrPath


class BaseReport:
    pass


class WorkspaceReport(BaseReport):
    ssas: BaseTabularModel
    rest_commands: Any


class LocalReport(BaseReport):
    ssas: LocalTabularModel
    static_elements: StaticElements
    _original_path: Optional["StrPath"] = None

    def __init__(self, ssas: LocalTabularModel, static_elements: StaticElements) -> None:
        self.ssas = ssas
        self.static_elements = static_elements

    @staticmethod
    def load_pbix(path: "StrPath") -> "LocalReport":
        server = get_or_create_local_server()
        ssas = server.load_pbix(path)
        static_elements = StaticElements(path)
        return LocalReport(ssas=ssas, static_elements=static_elements)

    def dump_pbix(self, path: "StrPath") -> None:
        pass
