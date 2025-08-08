import datetime
from typing import TYPE_CHECKING

from pbi_core.ssas.model_tables.base import SsasEditableRecord

from .enums import MemberType

if TYPE_CHECKING:
    from pbi_core.ssas.model_tables.role import Role


class RoleMembership(SsasEditableRecord):
    """TBD.

    SSAS spec: [Microsoft](https://learn.microsoft.com/en-us/openspecs/sql_server_protocols/ms-ssas-t/dbecc1f4-142b-4765-8374-a4d4dc51313b)
    """

    identity_provider: str
    member_id: str
    member_name: str
    member_type: MemberType
    role_id: int

    modified_time: datetime.datetime

    def role(self) -> "Role":
        return self.tabular_model.roles.find(self.role_id)
