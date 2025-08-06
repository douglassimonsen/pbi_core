import pathlib
import shutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import StrPath

    from .server import BaseServer


class BaseTabularModel:
    db_name: str
    server: "BaseServer"

    def __init__(self, db_name: str, server: "BaseServer") -> None:
        self.db_name = db_name
        self.server = server

    def save_pbix(self, path: "StrPath") -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"TabularModel(db_name={self.db_name}, server={self.server})"

    def to_local(self, pbix_path: pathlib.Path) -> "LocalTabularModel":
        return LocalTabularModel(self.db_name, self.server, pbix_path)


class LocalTabularModel(BaseTabularModel):
    pbix_path: pathlib.Path

    def __init__(self, db_name: str, server: "BaseServer", pbix_path: pathlib.Path) -> None:
        self.pbix_path = pbix_path
        super().__init__(db_name, server)

    def save_pbix(self, path: "StrPath") -> None:
        shutil.copy(self.pbix_path, path)
        self.server.save_pbix(path, self.db_name)  # type: ignore  # the server is always a local server in this case
