from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands


class PerspectiveColumn(SsasTable):
    _commands: SsasBaseCommands
