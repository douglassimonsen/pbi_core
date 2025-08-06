from ..server.tabular_model import SsasTable
from ._commands import SsasBaseCommands


class DetailRowDefinition(SsasTable):
    _commands: SsasBaseCommands

    @classmethod
    def _db_type_name(cls) -> str:
        return "DetailRowsDefinition"

    pass
