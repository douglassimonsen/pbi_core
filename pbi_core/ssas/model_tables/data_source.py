import datetime

from pbi_core.ssas.server.tabular_model import SsasRenameRecord


class DataSource(SsasRenameRecord):
    model_id: int
    name: str
    type: int
    connection_string: str
    impersonation_mode: int
    max_connections: int
    isolation: int
    timeout: int
    modified_time: datetime.datetime
