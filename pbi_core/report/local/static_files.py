from typing import TYPE_CHECKING

from pbi_core.logging import get_logger
from pbi_core.report.base import BaseReport
from pbi_core.static_files import StaticFiles

logger = get_logger()

if TYPE_CHECKING:
    from _typeshed import StrPath


class LocalStaticReport(BaseReport):
    """An instance of a PowerBI report from a local PBIX file.

    Args:
        static_files (StaticElements): An instance of all the static files (except DataModel) in the PBIX file

    Examples:
        ```python
        from pbi_core import LocalReport

        report = LocalReport.load_pbix("example.pbix")
        report.save_pbix("example_out.pbix")
        ```

    """

    static_files: StaticFiles
    """Classes representing the static design portions of the PBIX report"""

    def __init__(self, static_files: StaticFiles) -> None:
        self.static_files = static_files

    @staticmethod
    def load_pbix(path: "StrPath") -> "LocalStaticReport":
        logger.info("Loading PBIX Static Files", path=path)
        static_files = StaticFiles.load_pbix(path)
        return LocalStaticReport(static_files=static_files)

    def save_pbix(self, path: "StrPath", *, sync_ssas_changes: bool = True) -> None:
        """Creates a new PBIX with the information in this class to the given path.

        Examples:
            ```python

               from pbi_core import LocalReport

               report = LocalReport.load_pbix("example.pbix")
            ```
               report.save_pbix("example_out.pbix")

        Args:
            path (StrPath): the path (relative or absolute) to save the PBIX to
            sync_ssas_changes (bool, optional): whether to sync changes made in the SSAS model back to the PBIX file

        """
        msg = "save_pbix is not yet implemented"
        raise NotImplementedError(msg)
