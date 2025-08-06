from typing import TYPE_CHECKING, Any, ClassVar, Protocol

from structlog import get_logger

from pbi_core.ssas.server._commands import Command, Commands

if TYPE_CHECKING:
    from .tabular_model import BaseTabularModel

logger = get_logger()


class SsasTable(Protocol):
    """Specifies fields necessary to implement SSAS commands.

    This class needs to be a Protocol to allow type checking to validate
    that there's only a single __hash__ method defined, removing superfluous
    "Not Hashable" errors.

    """

    _read_only_fields: ClassVar[tuple[str, ...]] = ()
    _db_field_names: dict[str, str]
    _commands: Commands
    tabular_model: "BaseTabularModel"

    @classmethod
    def _db_type_name(cls) -> str: ...

    @staticmethod
    def render_xml_command(values: dict[str, Any], command: Command, db_name: str) -> str: ...

    def query_xml(self, query: str, db_name: str | None = None) -> None: ...

    def model_dump(self) -> dict[str, Any]: ...
