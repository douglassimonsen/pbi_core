from typing import Any
from xml.sax.saxutils import escape  # nosec

import jinja2

from pbi_core.attrs import define
from pbi_core.ssas.server._commands import Command


def python_to_xml(text: Any) -> str:
    """Implements basic XML transformation when returning data to SSAS backend.

    Converts:

    - True/False to true/false

    Args:
        text (Any): a value to be sent to SSAS

    Returns:
        str: A stringified, xml-safe version of the value

    """
    if text in {True, False}:
        return str(text).lower()
    if not isinstance(text, str):
        text = str(text)
    return escape(text)


ROW_TEMPLATE = jinja2.Template(
    """
<row xmlns="urn:schemas-microsoft-com:xml-analysis:rowset">
{%- for k, v in fields %}
  <{{k}}>{{v}}</{{k}}>
{%- endfor %}
</row>
""".lstrip(),
)


@define()
class CommandData:
    data: dict[str, str | int | bool | None]
    entity: str
    command: Command
    db_name: str

    def _get_row_xml(self, values: dict[str, Any]) -> str:
        fields: list[tuple[str, str]] = []
        for field_name, field_value in values.items():
            if field_name not in self.command.field_order:
                continue
            if field_value is None:
                continue
            fields.append((field_name, python_to_xml(field_value)))
        fields = self.command.sort(fields)
        return ROW_TEMPLATE.render(fields=fields)
