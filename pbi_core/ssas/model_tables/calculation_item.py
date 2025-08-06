from ..server.tabular_model import SsasTable
from ._commands import SsasRenameCommands


class CalculationItem(SsasTable):
    _commands: SsasRenameCommands
