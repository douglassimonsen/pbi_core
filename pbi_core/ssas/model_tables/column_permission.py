from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands


class ColumnPermission(SsasTable):
    _commands: SsasBaseCommands
