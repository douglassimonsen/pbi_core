import pathlib
from datetime import UTC, datetime  # type: ignore
from typing import TYPE_CHECKING, Optional

from .tabular_db import TabularDB

if TYPE_CHECKING:
    from _typeshed import StrPath


DT_FORMAT = "%Y-%m-%d_%H-%M-%S"


class BaseServer:
    """
    Base Server Interface containing the methods used outside of instance lifetime management
    """

    host: str
    port: int
    dbname: str

    def __init__(self, host: str, port: int, dbname: str) -> None:
        self.host = host
        self.port = port
        self.dbname = dbname

    def conn_str(self, database: Optional[str] = None) -> str:
        if database:
            return f"Provider=MSOLAP;Data Source={self.host}:{self.port};Initial Catalog={database}"
        else:
            return f"Provider=MSOLAP;Data Source={self.host}:{self.port};"

    def __repr__(self) -> str:
        return f"Server(host={self.port}, port={self.port}, db={self.dbname})"

    def query_dax(self, query: str, dbname: Optional[str] = None) -> None:
        pass

    def query_xml(self, query: str, dbname: Optional[str] = None) -> None:
        pass

    def databases(self) -> list[TabularDB]:
        return []


class LocalServer(BaseServer):
    pid: int
    kill_on_exit: bool
    _initial_time: datetime

    def __init__(
        self,
        host: str,
        port: int,
        dbname: str,
        pid: int,
        kill_on_exit: bool = True,
        _inital_time: Optional[datetime] = None,
    ) -> None:
        super().__init__(host, port, dbname)
        self.pid = pid
        self.kill_on_exit = kill_on_exit
        self._initial_time = _inital_time or datetime.now(UTC)
        super().__init__(host, port, dbname)

    def load_pbix(self, path: "StrPath", dbname: str) -> None:
        path = pathlib.Path(path)
        pass

    def save_pbix(self, path: "StrPath", dbname: str) -> None:
        path = pathlib.Path(path)
        pass
