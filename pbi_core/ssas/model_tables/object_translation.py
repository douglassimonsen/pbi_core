from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands


class ObjectTranslation(SsasTable):
    _commands: SsasBaseCommands
