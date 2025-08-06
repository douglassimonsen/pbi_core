import datetime

from pbi_core.ssas.server.tabular_model import SsasRenameRecord


class DataSource(SsasRenameRecord):
    """TBD.

    SSAS spec: https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/ee12dcb7-096e-4e4e-99a4-47caeb9390f5
    """

    model_id: int
    name: str
    type: int
    connection_string: str
    impersonation_mode: int
    max_connections: int
    isolation: int
    timeout: int
    modified_time: datetime.datetime
