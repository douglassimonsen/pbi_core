from ..server.tabular_model import SsasTable
from ._commands import NoCommands


class RelatedColumnDetail(SsasTable):
    _commands: NoCommands

    @classmethod
    def _db_type_name(cls) -> str:
        return "RelatedColumnDetails"
