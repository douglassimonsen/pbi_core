import pathlib
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Optional

import backoff
import bs4
import psutil

from ...logging import get_logger
from .._pyadomd import pyadomd
from ._physical_local_server import SSASProcess
from .tabular_model import BaseTabularModel, LocalTabularModel
from .utils import COMMAND_TEMPLATES, ROOT_FOLDER, SKU_ERROR, get_msmdsrv_info

logger = get_logger()

if TYPE_CHECKING:
    from _typeshed import StrPath


DT_FORMAT = "%Y-%m-%d_%H-%M-%S"


class BaseServer:
    """
    Base Server Interface containing the methods used outside of instance lifetime management
    """

    host: str
    "A hostname to the background SSAS instance"

    port: int
    "A Port to the background SSAS instance"

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

        self.check_ssas_sku()

    def conn_str(self, db_name: Optional[str] = None) -> str:
        """
        Formats the connection string for connecting to the background SSAS instance
        """
        if db_name:
            return f"Provider=MSOLAP;Data Source={self.host}:{self.port};Initial Catalog={db_name};"
        else:
            return f"Provider=MSOLAP;Data Source={self.host}:{self.port};"

    def conn(self, db_name: Optional[str] = None) -> pyadomd.Pyadomd:
        return pyadomd.Pyadomd(self.conn_str(db_name))

    def __repr__(self) -> str:
        return f"Server(host={self.host}:{self.port})"

    def query_dax(self, query: str, db_name: Optional[str] = None) -> list[dict[str, Any]]:
        with self.conn(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            data: list[tuple[Any]] = cursor.fetchall()
            columns: list[str] = [x[0] for x in cursor.description]
            return [dict(zip(columns, row)) for row in data]

    def query_xml(self, query: str, db_name: Optional[str] = None) -> bs4.BeautifulSoup:
        with self.conn(db_name) as conn:
            cursor = conn.cursor()
            return cursor.executeXML(query)

    def tabular_models(self) -> list[BaseTabularModel]:
        # Query based on https://learn.microsoft.com/en-us/previous-versions/sql/sql-server-2012/ms126314(v=sql.110)
        dbs = self.query_dax(COMMAND_TEMPLATES["list_dbs.xml"].render())
        return [BaseTabularModel(row["CATALOG_NAME"], self) for row in dbs]

    @backoff.on_exception(backoff.expo, ValueError, max_time=10)
    def check_ssas_sku(self) -> None:
        try:
            self.query_xml(
                COMMAND_TEMPLATES["image_save.xml"].render(
                    target_path="---", db_name="---"
                )  # specifically choosing non-existant values to verify we get at least one error
            )
        except pyadomd.AdomdErrorResponseException as e:  # type: ignore
            error_message = str(e.Message)
            if error_message == SKU_ERROR:
                return
            else:
                raise TypeError(f"Incorrect SKUVersion. We got the error: {error_message}")
        raise ValueError("Got a 'file not loaded' type error. Waiting")

    @staticmethod
    def sanitize_xml(xml_text: str) -> str:
        """
        Method to XML-encode characters like "&" so that the Adomd connection doesn't mangle the XMLA commands
        """
        return xml_text.replace("&", "&amp")

    @staticmethod
    def remove_invalid_db_name_chars(orig_db_name: str) -> str:
        """
        Utility function to convert a PBIX report name to a legible, but conforming name for the DB in the SSAS instance

        Note:
            Raises a warning if the db_name is changed to inform user that the db_name does not match their input
        """
        db_name = orig_db_name.replace("&", " ")[:100]
        db_name = db_name.strip()  # needed to find the correct name, since SSAS does stripping too
        if orig_db_name != db_name:
            logger.warn("db_name changed", original_name=orig_db_name, new_name=db_name)
        return db_name


class LocalServer(BaseServer):
    """
    A Server running locally on the user's machine.

    This subclass has the ability to load/dump Tabular Models
    to a PBIX file. Also creates a background SSAS instance and workspace to handle processing if none is provided.

    Args:
        kill_on_exit (bool): Indicates if the background SSAS instance handling processing should be terminated at the end of the python session
    """

    physical_process: SSASProcess
    """
    A Python class handling the lifetime of the SSAS Instance. Interacts with the SSAS instance only as a process
    """

    def __init__(
        self,
        host: str = "localhost",
        workspace_directory: Optional["StrPath"] = None,
        pid: Optional[int] = None,
        kill_on_exit: bool = True,
    ) -> None:
        if pid is not None:
            self.physical_process = SSASProcess(pid=pid, kill_on_exit=kill_on_exit)
        else:
            workspace_directory = workspace_directory or (
                ROOT_FOLDER / f"workspaces/{datetime.now(UTC).strftime(DT_FORMAT)}"
            )
            self.physical_process = SSASProcess(workspace_directory=workspace_directory, kill_on_exit=kill_on_exit)
        super().__init__(host, self.physical_process.port)

    def load_pbix(self, path: "StrPath", db_name: Optional[str] = None) -> LocalTabularModel:
        """
        Takes a Path to a PBIX report and loads the PBIX Datamodel to the SSAS instance in the SSASProcess
        """
        path = pathlib.Path(path)
        if db_name is None:
            db_name = path.stem
        db_name = self.remove_invalid_db_name_chars(db_name)
        self.query_xml(
            COMMAND_TEMPLATES["image_load.xml"].render(
                db_name=db_name, source_path=self.sanitize_xml(path.absolute().as_posix())
            )
        )
        logger.info("Tabular Model load complete")
        tab_model = LocalTabularModel(db_name=db_name, server=self, pbix_path=path)
        tab_model.sync_from()
        return tab_model

    def save_pbix(self, path: "StrPath", db_name: str) -> None:
        path = pathlib.Path(path)
        self.query_xml(
            COMMAND_TEMPLATES["image_save.xml"].render(
                db_name=db_name, target_path=self.sanitize_xml(path.absolute().as_posix())
            )
        )

    def __repr__(self) -> str:
        return f"LocalServer(port={self.port})"


def list_local_servers() -> list[LocalServer]:
    ret: list[LocalServer] = []
    for process in psutil.process_iter():
        if get_msmdsrv_info(process) is not None:
            ret.append(LocalServer(pid=process.pid, kill_on_exit=False))
    return ret


def get_or_create_local_server(kill_on_exit: bool = True) -> LocalServer:
    candidates: list[LocalServer] = list_local_servers()
    if candidates:
        return candidates[0]
    return LocalServer(kill_on_exit=kill_on_exit)


def terminate_all_local_servers() -> None:
    for server in list_local_servers():
        server.physical_process.terminate()
