import dataclasses
import pathlib
import socket
from typing import Optional

import jinja2
import psutil

COMMAND_DIR: pathlib.Path = pathlib.Path(__file__).parent / "command_templates"

COMMAND_TEMPLATES: dict[str, jinja2.Template] = {
    f.name: jinja2.Template(f.read_text()) for f in COMMAND_DIR.iterdir() if f.is_file()
}
ROOT_FOLDER = pathlib.Path(__file__).parents[2]
SKU_ERROR = "ImageLoad/ImageSave commands supports loading/saving data for Excel, Power BI Desktop or Zip files. File extension can be only .XLS?, .PBIX or .ZIP."


@dataclasses.dataclass
class ServerInfo:
    port: int
    workspace_directory: pathlib.Path


def get_msmdsrv_info(process: psutil.Process) -> Optional[ServerInfo]:
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
