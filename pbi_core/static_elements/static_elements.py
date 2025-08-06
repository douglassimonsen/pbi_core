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

    def __init__(self, path: "StrPath"):
        # should eventually convert into a load method with a standard init method
        zipfile = ZipFile(path, mode="r")

        layout_json = json.loads(zipfile.read("Report/Layout").decode(LAYOUT_ENCODING))
        self.layout = Layout.model_validate(layout_json)

        connections_json = json.loads(zipfile.read("Connections").decode("utf-8"))
        self.connections = Connections.model_validate(connections_json)

        major, minor = zipfile.read("Version").decode(LAYOUT_ENCODING).split(".")
        self.version = Version(int(major), int(minor))
        self.security_bindings = zipfile.read("SecurityBindings")

        self.content_types = BeautifulSoup(zipfile.read("[Content_Types].xml").decode("utf-8"), "lxml")

        metadata_json = json.loads(zipfile.read("Metadata").decode(LAYOUT_ENCODING))
        self.metadata = Metadata.model_validate(metadata_json)

        diagram_json = json.loads(zipfile.read("DiagramLayout").decode(LAYOUT_ENCODING))
        self.diagram_layout = DiagramLayout.model_validate(diagram_json)
