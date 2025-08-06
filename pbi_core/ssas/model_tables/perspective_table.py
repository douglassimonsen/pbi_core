from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands


class PerspectiveTable(SsasTable):
    _commands: SsasBaseCommands
