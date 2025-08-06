import dataclasses

import jinja2
from bs4 import BeautifulSoup

BASE_ALTER_TEMPLATE = jinja2.Template(
    """
<Batch Transaction="false" xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
  <Alter xmlns="http://schemas.microsoft.com/analysisservices/2014/engine">
    <DatabaseID>{{db_name}}</DatabaseID>
    {{entity_def}}
  </Alter>
</Batch>
"""
)

# note that Transaction = true. I think it's necessary, not very tested tbqh
BASE_REFRESH_TEMPLATE = jinja2.Template(
    """
<Batch Transaction="true" xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
  <Refresh xmlns="http://schemas.microsoft.com/analysisservices/2014/engine">
	<DatabaseID>{{db_name}}</DatabaseID>
    {{entity_def}}
  </Refresh>
</Batch>
"""
)
BASE_RENAME_TEMPLATE = jinja2.Template(
    """
<Batch Transaction="false" xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
  <Alter xmlns="http://schemas.microsoft.com/analysisservices/2014/engine">
    <DatabaseID>{{db_name}}</DatabaseID>
  </Alter>
  <Rename xmlns="http://schemas.microsoft.com/analysisservices/2014/engine">
    <DatabaseID>{{db_name}}</DatabaseID>
    {{entity_def}}
  </Rename>
</Batch>
    """
)
BASE_DELETE_TEMPLATE = jinja2.Template(
    """
<Batch Transaction="false" xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
  <Delete xmlns="http://schemas.microsoft.com/analysisservices/2014/engine">
    <DatabaseID>{{db_name}}</DatabaseID>
    {{entity_def}}
  </Delete>
</Batch>
    """
)
BASE_CREATE_TEMPLATE = jinja2.Template("")
base_commands = {
    "alter": BASE_ALTER_TEMPLATE,
    "create": BASE_CREATE_TEMPLATE,
    "delete": BASE_DELETE_TEMPLATE,
    "refresh": BASE_REFRESH_TEMPLATE,
    "rename": BASE_RENAME_TEMPLATE,
}


@dataclasses.dataclass
class Command:
    template: jinja2.Template
    base_template: jinja2.Template
    field_order: list[str]

    def sort(self, fields: list[tuple[str, str]]) -> list[tuple[str, str]]:
        return list(sorted(fields, key=lambda k: self.field_order.index(k[0])))


class NoCommands:
    def __init__(self, **kwargs: str) -> None:
        for field_name, template_text in kwargs.items():
            v = Command(
                template=jinja2.Template(template_text),
                base_template=base_commands[field_name],
                field_order=self.get_field_order(template_text),
            )
            self.__setattr__(field_name, v)

    @staticmethod
    def get_field_order(text: str) -> list[str]:
        """
        Gets the order of the fields for the command, based on the ``xs:sequence`` section of the XML command.
        """
        tree = BeautifulSoup(text, "xml")
        fields = tree.find_all("xs:complexType", {"name": "row"})[0].find_all("xs:element")
        return [field["name"] for field in fields]


class BaseCommands(NoCommands):
    alter: Command
    create: Command
    delete: Command


class RenameCommands(BaseCommands):
    rename: Command


class RefreshCommands(RenameCommands):
    refresh: Command


class ModelCommands(NoCommands):
    alter: Command
    refresh: Command
    rename: Command


Commands = BaseCommands | RenameCommands | RefreshCommands | ModelCommands
