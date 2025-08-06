import dataclasses
import pathlib
import socket
from typing import Any, Optional
from xml.sax.saxutils import escape  # nosec

import jinja2
import psutil

COMMAND_DIR: pathlib.Path = pathlib.Path(__file__).parent / "command_templates"

COMMAND_TEMPLATES: dict[str, jinja2.Template] = {
    f.name: jinja2.Template(f.read_text()) for f in COMMAND_DIR.iterdir() if f.is_file()
}
OBJECT_COMMAND_TEMPLATES: dict[str, dict[str, str]] = {
    folder.name: {f.name: f.read_text() for f in folder.iterdir() if f.is_file()}
    for folder in (COMMAND_DIR / "schema").iterdir()
    if folder.is_dir()
}
ROOT_FOLDER = pathlib.Path(__file__).parents[2]
SKU_ERROR = "ImageLoad/ImageSave commands supports loading/saving data for Excel, Power BI Desktop or Zip files. File extension can be only .XLS?, .PBIX or .ZIP."


@dataclasses.dataclass
class ServerInfo:
    """
    Basic information about an SSAS instance from its PID
    """

    port: int
    workspace_directory: pathlib.Path


def get_msmdsrv_info(process: psutil.Process) -> Optional[ServerInfo]:
    """
    Parses ``ServerInfo`` information from PID information.

    Note:
        This function currently assumes that the SSAS Process is called like
        ``pbi_core`` calls it. If you don't include the ``-s`` flag in the command,
        this function will fail
    """

    def check_ports(proc: psutil.Process) -> Optional[int]:
        ports = [
            conn.laddr.port
            for conn in proc.net_connections()
            if conn.status == "LISTEN"
            and conn.family == socket.AF_INET  # to only get the IPV4, not IPV6 version of the connection
        ]
        if len(ports) != 1:
            return None
        return ports[0]  # type: ignore

    def check_workspace(proc: psutil.Process) -> Optional[pathlib.Path]:
        try:
            exe_start_command: list[str] = proc.cmdline()
        except psutil.AccessDenied:
            return None

        if "-s" not in exe_start_command:
            return None
        return pathlib.Path(exe_start_command[exe_start_command.index("-s") + 1])

    if process.name() != "msmdsrv.exe":
        return None
    if (port := check_ports(process)) is None:
        return None
    if (workspace_dir := check_workspace(process)) is None:
        return None
    return ServerInfo(port, workspace_dir)


def python_to_xml(text: Any) -> str:
    """Implements basic XML transformation when returning data to SSAS backend.

    Converts:

    - True/False to true/false

    Args:
        x (Any): a value to be sent to SSAS

    Returns:
        str: A stringified, xml-safe version of the value

    """
    if text in (True, False):
        return str(text).lower()
    if isinstance(text, str):
        text = escape(text)
    return str(text)


ROW_TEMPLATE = jinja2.Template(
    """
<row xmlns="urn:schemas-microsoft-com:xml-analysis:rowset">
{%- for k, v in fields %}
    <{{k}}>{{v}}</{{k}}>
{%- endfor %}
</row>                     
"""
)
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
<Batch Transaction="false" xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">>
  <Rename xmlns="http://schemas.microsoft.com/analysisservices/2014/engine">
    <DatabaseID>{{db_name}}</DatabaseID>
    {{entity_def}}
  </Rename>
</Batch>
    """
)
