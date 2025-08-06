from typing import Optional

from ..server.tabular_model import SsasReadonlyTable


class CalcDependency(SsasReadonlyTable):
    database_name: str
    object_type: str
    table: Optional[str] = None
    object: str
    expression: Optional[str] = None
    referenced_object_type: str
    referenced_table: Optional[str] = None
    referenced_object: str
    referenced_expression: Optional[str] = None
