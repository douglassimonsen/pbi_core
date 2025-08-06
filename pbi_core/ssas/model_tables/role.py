from ..server.tabular_model import SsasTable
from ._commands import SsasRenameCommands


class Role(SsasTable):
    _commands: SsasRenameCommands
