from ..server.tabular_model import SsasTable
from ._commands import SsasRenameCommands


class Perspective(SsasTable):
    _commands: SsasRenameCommands
