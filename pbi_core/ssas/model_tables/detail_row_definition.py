from pbi_core.ssas.server.tabular_model import SsasEditableRecord


class DetailRowDefinition(SsasEditableRecord):
    @classmethod
    def _db_type_name(cls) -> str:
        return "DetailRowsDefinition"
