from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands


class TablePermission(SsasTable):
    _commands: SsasBaseCommands
