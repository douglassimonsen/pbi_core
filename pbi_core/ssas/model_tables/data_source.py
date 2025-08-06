from ..server.tabular_model import SsasTable
from ._base import SsasRenameCommands


class DataSource(SsasTable):
    _commands: SsasRenameCommands
