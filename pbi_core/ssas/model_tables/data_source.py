from ..server.tabular_model import SsasTable
from ._commands import SsasRenameCommands


class DataSource(SsasTable):
    _commands: SsasRenameCommands
