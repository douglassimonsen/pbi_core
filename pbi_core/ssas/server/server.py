import pathlib
from datetime import UTC, datetime  # type: ignore
from typing import TYPE_CHECKING, Optional

from ...logging import get_logger
from .tabular_db import TabularDB
from .utils import COMMAND_TEMPLATES

logger = get_logger()

if TYPE_CHECKING:
    from _typeshed import StrPath


DT_FORMAT = "%Y-%m-%d_%H-%M-%S"


class BaseServer:
    """
    Base Server Interface containing the methods used outside of instance lifetime management
    """

    host: str
    port: int
    db_name: str

    def __init__(self, host: str, port: int, db_name: str) -> None:
        self.host = host
        self.port = port
        self.db_name = db_name

    def conn_str(self, database: Optional[str] = None) -> str:
        if database:
            return f"Provider=MSOLAP;Data Source={self.host}:{self.port};Initial Catalog={database}"
        else:
            return f"Provider=MSOLAP;Data Source={self.host}:{self.port};"

    def __repr__(self) -> str:
        return f"Server(host={self.port}, port={self.port}, db={self.db_name})"

    def query_dax(self, query: str, db_name: Optional[str] = None) -> None:
        pass

    def query_xml(self, query: str, db_name: Optional[str] = None) -> None:
        pass

    def databases(self) -> list[TabularDB]:
        return []


class LocalServer(BaseServer):
    pid: int
    kill_on_exit: bool
    _initial_time: datetime

    def __init__(
        self, host: str = "localhost", port: int = -1, db_name: str = "dummy", pid: int = -1, kill_on_exit: bool = True
    ) -> None:
        super().__init__(host, port, db_name)
        self.pid = pid
        self.kill_on_exit = kill_on_exit
        super().__init__(host, port, db_name)

    @property
    def _default_db_name_suffix(self) -> str:
        return datetime.now(UTC).strftime(DT_FORMAT)

    def load_pbix(self, path: "StrPath", db_name: Optional[str] = None) -> None:
        path = pathlib.Path(path)
        if db_name is None:
            db_name = f"{path.stem}_{self._default_db_name_suffix}"
        db_name = self.remove_invalid_db_name_chars(db_name)
        self.query_xml(
            COMMAND_TEMPLATES["image_load"].render(
                db_name=db_name, source_path=self.sanitize_xml(path.absolute().as_posix())
            )
        )

    @staticmethod
    def sanitize_xml(xml_text: str) -> str:
        return xml_text.replace("&", "&amp")

    @staticmethod
    def remove_invalid_db_name_chars(orig_db_name: str) -> str:
        db_name = orig_db_name.replace("&", " ")[:100]
        db_name = db_name.strip()  # needed to find the correct name, since SSAS does stripping too
        if orig_db_name != db_name:
            logger.warn("db_name changed", original_name=orig_db_name, new_name=db_name)
        return db_name

    def save_pbix(self, path: "StrPath", db_name: str) -> None:
        path = pathlib.Path(path)
        pass
