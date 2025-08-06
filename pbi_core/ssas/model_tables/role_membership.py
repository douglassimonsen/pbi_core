from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands


class RoleMembership(SsasTable):
    _commands: SsasBaseCommands
