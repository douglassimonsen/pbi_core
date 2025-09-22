from typing import Any, ClassVar, Literal, Self

from attrs import field
from bs4 import BeautifulSoup
from structlog import get_logger

from pbi_core.attrs import BaseValidation, define
from pbi_core.lineage import LineageNode
from pbi_core.ssas.model_tables._group import IdBase
from pbi_core.ssas.server._commands import Command
from pbi_core.ssas.server.tabular_model import BaseTabularModel
from pbi_core.ssas.server.utils import ROW_TEMPLATE, python_to_xml

logger = get_logger()


@define()
class SsasTable(BaseValidation, IdBase):
    id: int
    """Unique identifier of the object."""

    tabular_model: BaseTabularModel = field(repr=False, eq=False, hash=False, init=False)
    _read_only_fields: ClassVar[tuple[str, ...]] = ()

    _db_field_names: ClassVar[dict[str, str]] = {}
    _repr_name_field: str = "name"

    @classmethod
    def _db_type_name(cls) -> str:
        return cls.__name__

    @classmethod
    def _db_command_obj_name(cls) -> str:
        """Returns the name of the object expected by their XMLA commands.

        Generally a simple pluralization, but occasionally different in subclasses.
        """
        return cls.__name__ + "s"

    def pbi_core_name(self) -> str:
        """Returns the name displayed in the PBIX report.

        Uses the _repr_name_field to determine the field to use.
        Defaults to self.name
        """
        return str(getattr(self, self._repr_name_field))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id}: {self.pbi_core_name()})"

    @classmethod
    def to_snake_case(cls: type[Self], raw_values: dict[str, Any]) -> dict[str, Any]:
        """Converts SnakeCase to snake_case.

        If a "special_cases" example appears, that transformation is applied.
        If the first character is capitalized, it is lower cased
        If any other character is capitalized, it is lower cased and prefixed with a "_"
        """

        def update_char(char: str, prev_char: str) -> str:
            if char.isupper() and prev_char.islower() and prev_char != "_":
                return f"_{char.lower()}"
            return char.lower()

        def case_helper(field_name: str) -> str:
            SPECIAL_CASES = {  # noqa: N806
                "owerBI": "owerbi",
                "KPIID": "KpiId",
            }
            for old_segment, new_segment in SPECIAL_CASES.items():
                field_name = field_name.replace(old_segment, new_segment)
            return "".join(
                update_char(curr, prev) for prev, curr in zip(" " + field_name[:-1], field_name, strict=False)
            ).strip("_")

        ret: dict[str, Any] = {}
        for field_name, field_value in raw_values.items():
            formatted_field_name = case_helper(field_name)
            if formatted_field_name != field_name:
                cls._db_field_names[formatted_field_name] = field_name
            ret[formatted_field_name] = field_value
        return ret

    @classmethod
    def pre_attrs(cls, raw_values: dict[str, Any]) -> dict[str, Any]:
        return cls.to_snake_case(raw_values)

    def query_dax(self, query: str, db_name: str | None = None) -> None:
        """Helper function to remove the ``.tabular_model.server`` required to run a DAX query from an SSAS element."""
        logger.debug("Executing DAX query", query=query, db_name=db_name)
        self.tabular_model.server.query_dax(query, db_name=db_name)

    def query_xml(self, query: str, db_name: str | None = None) -> BeautifulSoup:
        """Helper function to remove the ``.tabular_model.server`` required to run an XML query from an SSAS element."""
        logger.debug("Executing XML query", query=query, db_name=db_name)
        return self.tabular_model.server.query_xml(query, db_name)

    @staticmethod
    def _get_row_xml(values: dict[str, Any], command: Command) -> str:
        fields: list[tuple[str, str]] = []
        for field_name, field_value in values.items():
            if field_name not in command.field_order:
                continue
            if field_value is None:
                continue
            fields.append((field_name, python_to_xml(field_value)))
        fields = command.sort(fields)
        return ROW_TEMPLATE.render(fields=fields)

    @staticmethod
    def render_xml_command(values: dict[str, Any], command: Command, db_name: str) -> str:
        """XMLA commands: create/alter/delete/rename/refresh.

        Commands are generally in the form:
        <batch>
            <create/alter...>
                <db>
            </create/alter...>
            <entity-schema.../>
            <records.../>
        </batch>

        Entity schemas can be found at `pbi_core/ssas/server/command_templates/schema`
        """
        logger.debug(
            "Rendering XML command",
            db_name=db_name,
            fields=list(values.keys()),
        )
        xml_row = SsasTable._get_row_xml(values, command)
        xml_entity_definition = command.entity_template.render(rows=xml_row)
        return command.base_template.render(db_name=db_name, entity_def=xml_entity_definition)

    def get_lineage(self, lineage_type: Literal["children", "parents"]) -> LineageNode:
        """Creates a lineage node tracking the data parents/children of a record."""
        return LineageNode(self, lineage_type)

    def __hash__(self) -> int:
        return hash(self.id)

    def xml_fields(self) -> dict[str, Any]:
        base = self.model_dump().items()
        ret = {}
        for k, v in base:
            if k not in self._read_only_fields:
                ret[self._db_field_names.get(k, k)] = v
        return ret

    def modification_hash(self) -> int:
        """Returns a hash representing the current state of the object."""
        msg = "Subclasses must implement modification_hash()"
        raise NotImplementedError(msg)
