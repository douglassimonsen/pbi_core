from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands


class CalculationGroup(SsasTable):
    _commands: SsasBaseCommands
