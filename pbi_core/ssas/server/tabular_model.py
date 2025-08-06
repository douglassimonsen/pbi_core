import pathlib
import shutil
from typing import TYPE_CHECKING, Any, cast

from bs4 import BeautifulSoup, Tag

from ..model_tables import (
    Group,
    Table,
)
from .utils import COMMAND_TEMPLATES

if TYPE_CHECKING:
    from _typeshed import StrPath

    from .server import BaseServer


FIELD_TYPES = {"tables": Table}


class BaseTabularModel:
    db_name: str
    server: "BaseServer"

    tables: Group[Table]

    def __init__(self, db_name: str, server: "BaseServer") -> None:
        self.db_name = db_name
        self.server = server

    def save_pbix(self, path: "StrPath") -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"TabularModel(db_name={self.db_name}, server={self.server})"

    def to_local(self, pbix_path: pathlib.Path) -> "LocalTabularModel":
        return LocalTabularModel(self.db_name, self.server, pbix_path)

    def sync_from(self) -> None:
        xml_schema = self.server.query_xml(COMMAND_TEMPLATES["discover_schema.xml"].render(db_name=self.db_name))
        schema = discover_xml_to_dict(xml_schema)
        for field_name, type_instance in FIELD_TYPES.items():
            objects = [type_instance.model_validate(row) for row in schema[type_instance._db_type_name()]]
            setattr(self, field_name, objects)

    def sync_to(self) -> None:
        pass


class LocalTabularModel(BaseTabularModel):
    pbix_path: pathlib.Path

    def __init__(self, db_name: str, server: "BaseServer", pbix_path: pathlib.Path) -> None:
        self.pbix_path = pbix_path
        super().__init__(db_name, server)

    def save_pbix(self, path: "StrPath") -> None:
        shutil.copy(self.pbix_path, path)
        self.server.save_pbix(path, self.db_name)  # type: ignore  # the server is always a local server in this case


def discover_xml_to_dict(xml: BeautifulSoup) -> dict[str, list[dict[Any, Any]]]:
    assert xml.results is not None
    results: list[Tag] = list(xml.results)  # apparently, this is actually fine
    results[-1]["name"] = "CALC_DEPENDENCY"

    return {
        cast(str, table["name"]): [
            {field.name: field.text for field in row if field.name is not None} for row in table.find_all("row")
        ]
        for table in results
    }
