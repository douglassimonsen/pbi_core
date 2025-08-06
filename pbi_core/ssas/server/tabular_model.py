import pathlib
import shutil
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Type, cast

import pydantic
from bs4 import BeautifulSoup, Tag
from structlog import get_logger

from ...lineage import LineageNode, LineageType
from ._commands import BaseCommands, Command, ModelCommands, NoCommands, RefreshCommands, RenameCommands
from .utils import (
    COMMAND_TEMPLATES,
    OBJECT_COMMAND_TEMPLATES,
    ROW_TEMPLATE,
    python_to_xml,
)

logger = get_logger()
if TYPE_CHECKING:
    from _typeshed import StrPath

    from ..model_tables import (
        KPI,
        AlternateOf,
        Annotation,
        AttributeHierarchy,
        CalcDependency,
        CalculationGroup,
        CalculationItem,
        Column,
        ColumnPermission,
        Culture,
        DataSource,
        DetailRowDefinition,
        Expression,
        ExtendedProperty,
        FormatStringDefinition,
        Group,
        GroupByColumn,
        Hierarchy,
        Level,
        LinguisticMetadata,
        Measure,
        Model,
        ObjectTranslation,
        Partition,
        Perspective,
        PerspectiveColumn,
        PerspectiveHierarchy,
        PerspectiveMeasure,
        PerspectiveSet,
        PerspectiveTable,
        QueryGroup,
        RefreshPolicy,
        RelatedColumnDetail,
        Relationship,
        Role,
        RoleMembership,
        Set,
        Table,
        TablePermission,
        Variation,
    )
    from .server import BaseServer


class BaseTabularModel:
    db_name: str
    server: "BaseServer"
    model: "Model"
    alternate_ofs: "Group[AlternateOf]"
    annotations: "Group[Annotation]"
    attribute_hierarchies: "Group[AttributeHierarchy]"
    calc_dependencies: "Group[CalcDependency]"
    calculation_groups: "Group[CalculationGroup]"
    calculation_items: "Group[CalculationItem]"
    columns: "Group[Column]"
    column_permissions: "Group[ColumnPermission]"
    cultures: "Group[Culture]"
    data_sources: "Group[DataSource]"
    detail_row_definitions: "Group[DetailRowDefinition]"
    expressions: "Group[Expression]"
    extended_properties: "Group[ExtendedProperty]"
    format_string_definitions: "Group[FormatStringDefinition]"
    group_by_columns: "Group[GroupByColumn]"
    hierarchies: "Group[Hierarchy]"
    kpis: "Group[KPI]"
    levels: "Group[Level]"
    linguistic_metadata: "Group[LinguisticMetadata]"
    measures: "Group[Measure]"
    object_translations: "Group[ObjectTranslation]"
    partitions: "Group[Partition]"
    perspectives: "Group[Perspective]"
    perspective_columns: "Group[PerspectiveColumn]"
    perspective_hierarchies: "Group[PerspectiveHierarchy]"
    perspective_measures: "Group[PerspectiveMeasure]"
    perspective_sets: "Group[PerspectiveSet]"
    perspective_tables: "Group[PerspectiveTable]"
    query_groups: "Group[QueryGroup]"
    refresh_policies: "Group[RefreshPolicy]"
    related_column_details: "Group[RelatedColumnDetail]"
    relationships: "Group[Relationship]"
    roles: "Group[Role]"
    role_memberships: "Group[RoleMembership]"
    sets: "Group[Set]"
    tables: "Group[Table]"
    table_permissions: "Group[TablePermission]"
    variations: "Group[Variation]"

    def __init__(self, db_name: str, server: "BaseServer") -> None:
        self.db_name = db_name
        self.server = server

    def save_pbix(self, path: "StrPath") -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"TabularModel(db_name={self.db_name}, server={self.server})"

    def to_local(self, pbix_path: pathlib.Path) -> "LocalTabularModel":
        return LocalTabularModel(self.db_name, self.server, pbix_path)

    def sync_from(self) -> None:
        from ..model_tables import FIELD_TYPES
        from ..model_tables._group import Group

        xml_schema = self.server.query_xml(COMMAND_TEMPLATES["discover_schema.xml"].render(db_name=self.db_name))
        schema = discover_xml_to_dict(xml_schema)
        for field_name, type_instance in FIELD_TYPES.items():
            if field_name == "model":
                object = type_instance.model_validate({
                    **schema[type_instance._db_type_name()][0],
                    "_tabular_model": self,
                })
                setattr(self, field_name, object)
            else:
                objects = Group([
                    type_instance.model_validate({**row, "_tabular_model": self})
                    for row in schema[type_instance._db_type_name()]
                ])
                setattr(self, field_name, objects)


class LocalTabularModel(BaseTabularModel):
    pbix_path: pathlib.Path

    def __init__(self, db_name: str, server: "BaseServer", pbix_path: pathlib.Path) -> None:
        self.pbix_path = pbix_path
        super().__init__(db_name, server)

    def save_pbix(self, path: "StrPath") -> None:
        shutil.copy(self.pbix_path, path)
        self.server.save_pbix(path, self.db_name)  # type: ignore  # the server is always a local server in this case


def discover_xml_to_dict(xml: BeautifulSoup) -> dict[str, list[dict[Any, Any]]]:
    assert xml.results is not None
    results: list[Tag] = list(xml.results)  # type: ignore
    results[-1]["name"] = "CalcDependency"
    ret = {
        cast(str, table["name"]): [
            {field.name: field.text for field in row if field.name is not None} for row in table.find_all("row")
        ]
        for table in results
    }
    for i, row in enumerate(ret["CalcDependency"]):
        row["id"] = i
    return ret


SsasConfig = pydantic.ConfigDict(
    arbitrary_types_allowed=True,
    extra="forbid",
    use_enum_values=False,
    json_schema_mode_override="serialization",
    validate_assignment=True,
    protected_namespaces=(),
)


class SsasTable(pydantic.BaseModel):
    model_config = SsasConfig
    tabular_model: "BaseTabularModel"
    _read_only_fields: ClassVar[tuple[str, ...]] = tuple()
    _commands: Any
    id: int
    _db_field_names: ClassVar[dict[str, str]] = {}
    _repr_name_field: str = "name"

    @classmethod
    def _db_type_name(cls) -> str:
        return cls.__name__

    @classmethod
    def _db_plural_type_name(cls) -> str:
        return cls.__name__ + "s"

    def pbi_core_name(self) -> str:
        return getattr(self, self._repr_name_field)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pbi_core_name()})"

    @pydantic.model_validator(mode="before")
    def to_snake_case(cls: "SsasTable", raw_values: dict[str, Any]) -> dict[str, Any]:
        def update_char(char: str, prev_char: str) -> str:
            if char.isupper() and prev_char.islower() and prev_char != "_":
                return f"_{char.lower()}"
            else:
                return char.lower()

        def case_helper(field_name: str) -> str:
            special_cases = {
                "owerBI": "owerbi",
            }
            for old_segment, new_segment in special_cases.items():
                field_name = field_name.replace(old_segment, new_segment)
            field_name = "".join(
                update_char(curr, prev) for prev, curr in zip(" " + field_name[:-1], field_name)
            ).strip("_")

            return field_name

        ret = {}
        for field_name, field_value in raw_values.items():
            formatted_field_name = case_helper(field_name)
            if formatted_field_name != field_name:
                cls._db_field_names[formatted_field_name] = field_name
            ret[formatted_field_name] = field_value
        return ret

    def query_dax(self, query: str, db_name: Optional[str] = None) -> None:
        self.tabular_model.server.query_dax(query, db_name)

    def query_xml(self, query: str, db_name: Optional[str] = None) -> None:
        self.tabular_model.server.query_xml(query, db_name)

    @staticmethod
    def render_xml_command(values: dict[str, Any], command: Command, db_name: str) -> str:
        fields = []
        for field_name, field_value in values.items():
            if field_name not in command.field_order:
                continue
            if field_value is None:
                continue
            fields.append((field_name, python_to_xml(field_value)))
        fields = command.sort(fields)
        xml_row = ROW_TEMPLATE.render(fields=fields)
        xml_entity_definition = command.template.render(rows=xml_row)
        return command.base_template.render(db_name=db_name, entity_def=xml_entity_definition)

    def get_lineage(self, lineage_type: LineageType) -> LineageNode:
        return LineageNode(self, lineage_type)


class SsasAlter(SsasTable):
    def alter(self) -> None:
        data = {
            self._db_field_names.get(k, k): v for k, v in self.model_dump().items() if k not in self._read_only_fields
        }
        xml_command = self.render_xml_command(
            data,
            self._commands.alter,
            self.tabular_model.db_name,
        )
        logger.info("Syncing Alter Changes to SSAS", obj=self._db_type_name())
        self.query_xml(xml_command, db_name=self.tabular_model.db_name)


class SsasRename(SsasTable):
    _db_name_field: str = "not_defined"

    def rename(self) -> None:
        data = {
            self._db_field_names.get(k, k): v for k, v in self.model_dump().items() if k not in self._read_only_fields
        }
        xml_command = self.render_xml_command(
            data,
            self._commands.rename,
            self.tabular_model.db_name,
        )
        logger.info("Syncing Rename Changes to SSAS", obj=self._db_type_name())
        self.query_xml(xml_command, db_name=self.tabular_model.db_name)


class SsasCreate(SsasTable):
    @classmethod
    def create(cls: Type["SsasCreate"], tabular_model: "BaseTabularModel", **kwargs: dict[str, Any]) -> None:
        # data = {
        #     cls._db_field_names.get(k, k): v for k, v in kwargs.items() if k not in cls._read_only_fields
        # }
        # xml_command = cls.render_xml_command(
        #     data,
        #     cls._commands.rename,
        #     tabular_model.db_name,
        # )
        # logger.info("Syncing Rename Changes to SSAS", obj=cls._db_type_name())
        # tabular_model.server.query_xml(xml_command, db_name=tabular_model.db_name)
        pass


class SsasDelete(SsasTable):
    _db_id_field: str = "ID"

    def delete(self) -> None:
        data = {k: v for k, v in self.model_dump().items() if k == self._db_id_field}
        xml_command = self.render_xml_command(
            data,
            self._commands.delete,
            self.tabular_model.db_name,
        )
        logger.info("Syncing Delete Changes to SSAS", obj=self._db_type_name())
        self.query_xml(xml_command, db_name=self.tabular_model.db_name)


class SsasRefresh(SsasTable):
    def refresh(self) -> None:
        pass


class SsasReadonlyTable(SsasTable):
    _commands: NoCommands


class SsasBaseTable(SsasCreate, SsasAlter, SsasDelete):
    _commands: BaseCommands

    def model_post_init(self, __context: Any) -> None:
        templates = OBJECT_COMMAND_TEMPLATES.get(self._db_plural_type_name(), {})

        self._commands = BaseCommands(
            alter=templates["alter.xml"],
            create=templates["create.xml"],
            delete=templates["delete.xml"],
        )


class SsasRenameTable(SsasCreate, SsasAlter, SsasDelete, SsasRename):
    _commands: RenameCommands

    def model_post_init(self, __context: Any) -> None:
        templates = OBJECT_COMMAND_TEMPLATES.get(self._db_plural_type_name(), {})

        self._commands = RenameCommands(
            alter=templates["alter.xml"],
            create=templates["create.xml"],
            delete=templates["delete.xml"],
            rename=templates["rename.xml"],
        )


class SsasRefreshTable(SsasCreate, SsasAlter, SsasDelete, SsasRename, SsasRefresh):
    _commands: RefreshCommands

    def model_post_init(self, __context: Any) -> None:
        templates = OBJECT_COMMAND_TEMPLATES.get(self._db_plural_type_name(), {})

        self._commands = RefreshCommands(
            alter=templates["alter.xml"],
            create=templates["create.xml"],
            delete=templates["delete.xml"],
            rename=templates["rename.xml"],
            refresh=templates["refresh.xml"],
        )


class SsasModelTable(SsasAlter, SsasRefresh, SsasRename):
    _commands: ModelCommands

    def model_post_init(self, __context: Any) -> None:
        templates = OBJECT_COMMAND_TEMPLATES.get(self._db_plural_type_name(), {})

        self._commands = ModelCommands(
            alter=templates["alter.xml"],
            refresh=templates["refresh.xml"],
            rename=templates["rename.xml"],
        )
