from pbi_core.ssas.server.tabular_model import SsasEditableRecord


class DetailRowDefinition(SsasEditableRecord):
    """TBD.

    SSAS spec: https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/7eb1e044-4eed-467d-b10f-ce208798ddb0
    """

    @classmethod
    def _db_type_name(cls) -> str:
        return "DetailRowsDefinition"
