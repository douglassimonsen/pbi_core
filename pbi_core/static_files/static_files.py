import json
import zipfile
from dataclasses import dataclass
from typing import TYPE_CHECKING
from zipfile import ZipFile

from bs4 import BeautifulSoup

from .file_classes import Connections, DiagramLayout, Metadata, Settings
from .file_classes.theme import Theme
from .layout._base_node import _set_parents  # type: ignore
from .layout.layout import Layout

if TYPE_CHECKING:
    from _typeshed import StrPath

LAYOUT_ENCODING = "utf-16-le"


@dataclass
class Version:
    major: int
    minor: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"


class StaticFiles:
    content_types: BeautifulSoup
    connections: Connections
    # no datamodel, that's handled by the ssas folder
    diagram_layout: DiagramLayout
    layout: Layout
    metadata: Metadata
    version: Version
    security_bindings: bytes
    settings: Settings
    themes: dict[str, Theme]

    def __init__(
        self,
        content_types: BeautifulSoup,
        connections: Connections,
        diagram_layout: DiagramLayout,
        layout: Layout,
        metadata: Metadata,
        version: Version,
        security_bindings: bytes,
        settings: Settings,
        themes: dict[str, Theme],
    ):
        self.content_types = content_types
        self.connections = connections
        self.diagram_layout = diagram_layout
        self.layout = layout
        self.metadata = metadata
        self.version = version
        self.security_bindings = security_bindings
        self.settings = settings
        self.themes = themes

    @staticmethod
    def load_pbix(path: "StrPath") -> "StaticFiles":
        zipfile = ZipFile(path, mode="r")

        themes: dict[str, Theme] = {}
        theme_paths = [
            x.split("/")[-1]
            for x in zipfile.namelist()
            if x.startswith("Report/StaticResources/SharedResources/BaseThemes")
        ]
        for theme_path in theme_paths:
            theme_json = json.loads(
                zipfile.read(f"Report/StaticResources/SharedResources/BaseThemes/{theme_path}").decode("utf-8")
            )
            themes[theme_path] = Theme.model_validate(theme_json)

        layout_json = json.loads(zipfile.read("Report/Layout").decode(LAYOUT_ENCODING))
        layout = Layout.model_validate(layout_json)
        _set_parents(layout, None, [])  # type: ignore

        connections_json = json.loads(zipfile.read("Connections").decode("utf-8"))
        connections = Connections.model_validate(connections_json)

        major, minor = zipfile.read("Version").decode(LAYOUT_ENCODING).split(".")
        version = Version(int(major), int(minor))

        security_bindings = zipfile.read("SecurityBindings")

        content_types = BeautifulSoup(zipfile.read("[Content_Types].xml").decode("utf-8"), "lxml")

        metadata_json = json.loads(zipfile.read("Metadata").decode(LAYOUT_ENCODING))
        metadata = Metadata.model_validate(metadata_json)

        diagram_json = json.loads(zipfile.read("DiagramLayout").decode(LAYOUT_ENCODING))
        diagram_layout = DiagramLayout.model_validate(diagram_json)

        settings_json = json.loads(zipfile.read("Settings").decode(LAYOUT_ENCODING))
        settings = Settings.model_validate(settings_json)
        return StaticFiles(
            content_types, connections, diagram_layout, layout, metadata, version, security_bindings, settings, themes
        )

    def save_pbix(self, path: "StrPath") -> None:
        """
        We use "a" as the write mode because the ssas.save_pbix method already creates a PBIX with the datamodel subfile
        """
        data: dict[str, bytes] = {}
        with zipfile.ZipFile(path, "r", compression=zipfile.ZIP_DEFLATED) as zf:
            for f in zf.namelist():
                data[f] = zf.read(f)
        # breakpoint()
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("Settings", self.settings.model_dump_json().encode(LAYOUT_ENCODING))
            zf.writestr("Connections", self.connections.model_dump_json().encode("utf-8"))
            zf.writestr("Version", str(self.version).encode(LAYOUT_ENCODING))
            zf.writestr(
                "DiagramLayout", self.diagram_layout.model_dump_json().encode(LAYOUT_ENCODING)
            )  # has null nodeLineageTag that the source doesn't
            for path_name, theme_info in self.themes.items():
                zf.writestr(
                    f"Report/StaticResources/SharedResources/BaseThemes/{path_name}",
                    theme_info.model_dump_json().encode("utf-8"),
                )
            zf.writestr("DataModel", data["DataModel"])
            zf.writestr("Report/Layout", self.layout.model_dump_json().encode(LAYOUT_ENCODING))
            zf.writestr(
                "[Content_Types].xml", data["[Content_Types].xml"]
            )  # str(self.connections).encode("utf-8") needs to converted back to XML before being written

        exit()
        return
