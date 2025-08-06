from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands


class RefreshPolicy(SsasTable):
    _commands: SsasBaseCommands
