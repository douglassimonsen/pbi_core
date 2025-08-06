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
    """
    An instance of a PowerBI report from a local PBIX file.

    Args:
        ssas (LocalTabularModel): An instance of a local SSAS instance
        static_elements (StaticElements): An instance of all the static files (except DataModel) in the PBIX file

    Examples:
        .. code-block:: python
           :linenos:

           from pbi_core import LocalReport

           report = LocalReport.load_pbix("example.pbix")

    """

    ssas: LocalTabularModel
    static_elements: StaticElements
    _original_path: Optional["StrPath"] = None

    def __init__(self, ssas: LocalTabularModel, static_elements: StaticElements) -> None:
        self.ssas = ssas
        self.static_elements = static_elements

    @staticmethod
    def load_pbix(path: "StrPath", kill_ssas_on_exit: bool = True) -> "LocalReport":
        """
        Creates a ``LocalReport`` instance from a PBIX file.

        Args:
            path (StrPath): The absolute or local path to the PBIX report
            kill_ssas_on_exit (bool, optional): The LocalReport object depends on a ``msmdsrv.exe`` process that is independent of the Python session process. If this function creates a new ``msmdsrv.exe`` instance and kill_ssas_on_exit is true, the process will be killed on exit.

        """
        server = get_or_create_local_server(kill_on_exit=kill_ssas_on_exit)
        ssas = server.load_pbix(path)
        static_elements = StaticElements.load_pbix(path)
        return LocalReport(ssas=ssas, static_elements=static_elements)

    def save_pbix(self, path: "StrPath") -> None:
        self.static_elements.save_pbix(path)
        self.ssas.save_pbix(path)
