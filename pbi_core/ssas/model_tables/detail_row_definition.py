from ..server.tabular_model import SsasBaseTable


class DetailRowDefinition(SsasBaseTable):
    @classmethod
    def _db_type_name(cls) -> str:
        return "DetailRowsDefinition"
