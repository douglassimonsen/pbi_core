"""
Copyright 2020 SCOUT
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# mypy: ignore-errors
from enum import IntEnum
from pathlib import Path
from sys import path
from typing import Any, Iterator, NamedTuple, Optional, Self, TypeVar

import clr  # type: ignore[import-untyped]
from bs4 import BeautifulSoup

from ...logging import get_logger
from .c_sharp_type_mapping import adomd_type_map, convert

logger = get_logger()
T = TypeVar("T")


path.append(str(Path(__file__).parent)[2:])
clr.AddReference("Microsoft.AnalysisServices.AdomdClient")  # type: ignore
from Microsoft.AnalysisServices.AdomdClient import (  # type: ignore  # noqa: E402
    AdomdCommand,
    AdomdConnection,
    AdomdErrorResponseException,  # noqa: F401
    AdomdTransaction,
)

__all__ = ["AdomdErrorResponseException"]


class Description(NamedTuple):
    """
    :param [name]: Column name
    :param [type_code]: The column data type
    """

    name: str
    type_code: str


class TypedAdomdTransaction(AdomdTransaction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TypedAdomdConnection(AdomdConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def BeginTransaction(self) -> TypedAdomdTransaction:
        return super().BeginTransaction()


class Cursor:
    def __init__(self, connection: TypedAdomdConnection):
        self._conn = connection
        self._description: list[Description] = []

    def close(self) -> None:
        if self.is_closed:
            return
        self._reader.Close()

    def executeXML(self, query: str, query_name: Optional[str] = None) -> BeautifulSoup:
        def _clean_name(name: str) -> str:
            name_parts = name.split("_")
            for i, e in enumerate(name_parts):
                if len(e) == 5 and e[0] == "x" and all(c in "0123456789ABCDEF" for c in e[1:]):
                    name_parts[i] = chr(int(e[1:], 16))
            return "_".join(name_parts)

        query_name = query_name or ""
        logger.debug("execute XML query", query_name=query_name)
        self._cmd = AdomdCommand(query, self._conn)
        self._reader = self._cmd.ExecuteXmlReader()
        logger.debug("reading query", query_name=query_name)
        lines = [self._reader.ReadOuterXml()]
        while lines[-1] != "":
            lines.append(self._reader.ReadOuterXml())
        ret = BeautifulSoup("".join(lines), "xml")
        for node in ret.find_all():
            if node.name is not None:
                node.name = _clean_name(node.name)
        return ret

    def executeDAX(self, query: str, query_name: Optional[str] = None) -> Self:
        query_name = query_name or ""
        logger.debug("execute DAX query", query_name=query_name)
        self._cmd = AdomdCommand(query, self._conn)
        self._reader = self._cmd.ExecuteReader()
        self._field_count = self._reader.FieldCount

        logger.debug("reading query", query_name=query_name)
        for i in range(self._field_count):
            self._description.append(
                Description(
                    self._reader.GetName(i),
                    adomd_type_map[self._reader.GetFieldType(i).ToString()].type_name,
                )
            )
        return self

    def fetchone(self) -> Iterator[tuple[Any, ...]]:
        while self._reader.Read():
            yield tuple(
                convert(
                    self._reader.GetFieldType(i).ToString(),
                    self._reader[i],
                    adomd_type_map,
                )
                for i in range(self._field_count)
            )

    def fetchmany(self, size: int = 1) -> list[tuple[Any, ...]]:
        ret: list[tuple[Any, ...]] = []
        try:
            for _ in range(size):
                ret.append(next(self.fetchone()))
        except StopIteration:
            pass
        return ret

    def fetchall(self) -> list[tuple[Any, ...]]:
        """
        Fetches all the rows from the last executed query
        """
        # mypy issues with list comprehension :-(
        return [i for i in self.fetchone()]  # type: ignore

    @property
    def is_closed(self) -> bool:
        try:
            state: bool = self._reader.IsClosed
        except AttributeError:
            return True
        return state

    @property
    def description(self) -> list[Description]:
        return self._description

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


class AdmomdState(IntEnum):
    OPEN = 1
    CLOSED = 0


class Pyadomd:
    def __init__(self, conn_str: str):
        self.conn = AdomdConnection(conn_str)

    def close(self) -> None:
        """
        Closes the connection
        """
        self.conn.Close()
        self.conn.Dispose()

    def open(self) -> None:
        """
        Opens the connection
        """
        self.conn.Open()

    def cursor(self) -> Cursor:
        """
        Creates a cursor object
        """
        c = Cursor(self.conn)
        return c

    @property
    def state(self) -> AdmomdState:
        """
        1 = Open
        0 = Closed
        """
        return AdmomdState(self.conn.State)

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
