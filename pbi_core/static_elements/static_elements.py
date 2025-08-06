import json
from dataclasses import dataclass
from typing import TYPE_CHECKING
from zipfile import ZipFile

from bs4 import BeautifulSoup

from .file_classes import Connections, DiagramLayout, Metadata, Settings
from .layout.layout import Layout

if TYPE_CHECKING:
    from _typeshed import StrPath

LAYOUT_ENCODING = "utf-16-le"


@dataclass
class Version:
    major: int
    minor: int


class StaticElements:
    content_types: BeautifulSoup
    connections: Connections
    # no datamodel, that's handled by the ssas folder
    diagram_layout: DiagramLayout
    layout: Layout
    metadata: Metadata
    version: Version
    security_bindings: bytes
    settings: Settings

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
    ):
        self.content_types = content_types
        self.connections = connections
        self.diagram_layout = diagram_layout
        self.layout = layout
        self.metadata = metadata
        self.version = version
        self.security_bindings = security_bindings
        self.settings = settings

    @staticmethod
    def load_pbix(path: "StrPath") -> "StaticElements":
        zipfile = ZipFile(path, mode="r")

        layout_json = json.loads(zipfile.read("Report/Layout").decode(LAYOUT_ENCODING))
        layout = Layout.model_validate(layout_json)

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

        diagram_json = json.loads(zipfile.read("Settings").decode(LAYOUT_ENCODING))
        settings = Settings.model_validate(diagram_json)
        return StaticElements(
            content_types, connections, diagram_layout, layout, metadata, version, security_bindings, settings
        )

    def save_pbix(self, path: "StrPath") -> None:
        pass
