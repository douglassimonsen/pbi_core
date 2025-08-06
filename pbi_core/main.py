from typing import TYPE_CHECKING, Any

from .logging import get_logger
from .ssas.server import BaseTabularModel, LocalTabularModel, get_or_create_local_server
from .static_files import StaticFiles

logger = get_logger()

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
        static_files (StaticElements): An instance of all the static files (except DataModel) in the PBIX file

    Examples:
        .. code-block:: python
           :linenos:

           from pbi_core import LocalReport

           report = LocalReport.load_pbix("example.pbix")

    """

    ssas: LocalTabularModel
    """An instance of a local SSAS Server"""

    static_files: StaticFiles
    """Classes representing the static design portions of the PBIX report"""

    def __init__(self, ssas: LocalTabularModel, static_files: StaticFiles) -> None:
        self.ssas = ssas
        self.static_files = static_files

    @staticmethod
    def load_pbix(path: "StrPath", kill_ssas_on_exit: bool = True) -> "LocalReport":
        """
        Creates a ``LocalReport`` instance from a PBIX file.

        Args:
            path (StrPath): The absolute or local path to the PBIX report
            kill_ssas_on_exit (bool, optional): The LocalReport object depends on a ``msmdsrv.exe`` process that is independent of the Python session process. If this function creates a new ``msmdsrv.exe`` instance and kill_ssas_on_exit is true, the process will be killed on exit.

        Returns:
            LocalReport: the local PBIX class
        """
        logger.info("Loading PBIX", path=path)
        server = get_or_create_local_server(kill_on_exit=kill_ssas_on_exit)
        ssas = server.load_pbix(path)
        static_files = StaticFiles.load_pbix(path)
        return LocalReport(ssas=ssas, static_files=static_files)

    def save_pbix(self, path: "StrPath") -> None:
        """
        Creates a new PBIX with the information in this class to the given path.

        Args:
            path (StrPath): the path (relative or absolute) to save the PBIX to
        """
        self.static_files.save_pbix(path)
        self.ssas.save_pbix(path)
