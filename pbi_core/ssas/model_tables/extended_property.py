from ..server.tabular_model import SsasTable
from ._commands import SsasRenameCommands


class ExtendedProperty(SsasTable):
    _commands: SsasRenameCommands
