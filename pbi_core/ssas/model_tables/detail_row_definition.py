from ..server.tabular_model import SsasTable


class DetailRowDefinition(SsasTable):
    @classmethod
    def _db_type_name(cls) -> str:
        return "DetailRowsDefinition"

    pass
