import dataclasses

import jinja2
from bs4 import BeautifulSoup


@dataclasses.dataclass
class Command:
    template: jinja2.Template
    field_order: list[str]

    def sort(self, fields: list[str]) -> list[str]:
        return list(sorted(fields, key=lambda k: self.field_order.index(k[0])))


class NoCommands:
    def __init__(self, **kwargs: str) -> None:
        for field_name, template_text in kwargs.items():
            v = Command(template=jinja2.Template(template_text), field_order=self.get_field_order(template_text))
            self.__setattr__(field_name, v)

    @staticmethod
    def get_field_order(text: str) -> list[str]:
        tree = BeautifulSoup(text, "xml")
        fields = tree.find_all("xs:complexType", {"name": "row"})[0].find_all("xs:element")
        return [field["name"] for field in fields]


class SsasBaseCommands(NoCommands):
    alter: Command
    create: Command
    delete: Command


class SsasRenameCommands(SsasBaseCommands):
    rename: Command


class SsasRefreshCommands(SsasRenameCommands):
    refresh: Command


class SsasModelCommands(NoCommands):
    alter: Command
    refresh: Command
    rename: Command


SsasCommands = SsasBaseCommands | SsasRenameCommands | SsasRefreshCommands | SsasModelCommands
