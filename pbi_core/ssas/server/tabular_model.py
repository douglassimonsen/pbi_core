import pathlib
import shutil
from typing import TYPE_CHECKING, Any, ClassVar, cast

import pydantic
from bs4 import BeautifulSoup, Tag

from .utils import COMMAND_TEMPLATES, OBJECT_COMMAND_TEMPLATES

if TYPE_CHECKING:
    from _typeshed import StrPath

    from ..model_tables import (
        KPI,
        AlternateOf,
        Annotation,
        AttributeHierarchy,
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

        xml_schema = self.server.query_xml(COMMAND_TEMPLATES["discover_schema.xml"].render(db_name=self.db_name))
        schema = discover_xml_to_dict(xml_schema)
        for field_name, type_instance in FIELD_TYPES.items():
            objects = [
                type_instance.model_validate({**row, "_tabular_model": self})
                for row in schema[type_instance._db_type_name()]
            ]
            setattr(self, field_name, objects)

    def sync_to(self) -> None:
        from ..model_tables import FIELD_TYPES

        for field_name in FIELD_TYPES.keys():
            data = cast(list[SsasTable], getattr(self, field_name))
            for record in data:
                record.sync_to()


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
    results: list[Tag] = list(xml.results)  # apparently, this is actually fine
    results[-1]["name"] = "CALC_DEPENDENCY"

    return {
        cast(str, table["name"]): [
            {field.name: field.text for field in row if field.name is not None} for row in table.find_all("row")
        ]
        for table in results
    }


SsasConfig = pydantic.ConfigDict(
    arbitrary_types_allowed=True,
    extra="forbid",
    use_enum_values=False,
    json_schema_mode_override="serialization",
    validate_assignment=True,
    protected_namespaces=(),
)


class SsasTable(pydantic.BaseModel):  # type: ignore
    model_config = SsasConfig
    tabular_model: "BaseTabularModel"
    _read_only_fields: ClassVar[tuple[str, ...]] = tuple()
    id: int
    _commands: Any

    @classmethod
    def _db_type_name(cls) -> str:
        return cls.__name__

    @classmethod
    def _db_plural_type_name(cls) -> str:
        return cls.__name__ + "s"

    @pydantic.model_validator(mode="before")  # type: ignore
    def to_snake_case(cls: "SsasTable", raw_values: dict[str, Any]) -> dict[str, Any]:
        def case_helper(field_name: str) -> str:
            special_cases = {
                "owerBI": "owerbi",
                "ID": "Id",
                "MDX": "Mdx",
                "KPI": "Kpi",
            }
            for old_segment, new_segment in special_cases.items():
                field_name = field_name.replace(old_segment, new_segment)
            field_name = "".join(f"_{c.lower()}" if c.isupper() else c for c in field_name).strip("_")

            return field_name

        return {case_helper(field_name): field_value for field_name, field_value in raw_values.items()}

    def sync_to(self) -> "SsasTable":
        return self

    def model_post_init(self, __context: Any) -> None:
        from ..model_tables import _base

        if "_commands" not in self.__annotations__:
            return

        templates = OBJECT_COMMAND_TEMPLATES[self._db_plural_type_name()]
        match self.__annotations__["_commands"]:
            case _base.SsasRefreshCommands:
                self._commands = _base.SsasRefreshCommands(
                    alter=templates["alter.xml"],
                    create=templates["create.xml"],
                    delete=templates["delete.xml"],
                    rename=templates["rename.xml"],
                    refresh=templates["refresh.xml"],
                )
            case _base.SsasRenameCommands:
                self._commands = _base.SsasRenameCommands(
                    alter=templates["alter.xml"],
                    create=templates["create.xml"],
                    delete=templates["delete.xml"],
                    rename=templates["rename.xml"],
                )
            case _base.SsasBaseCommands:
                self._commands = _base.SsasBaseCommands(
                    alter=templates["alter.xml"], create=templates["create.xml"], delete=templates["delete.xml"]
                )
            case _base.SsasModelCommands:
                self._commands = _base.SsasModelCommands(
                    alter=templates["alter.xml"], refresh=templates["refresh.xml"], rename=templates["rename.xml"]
                )
            case _:
                raise ValueError(f"Unknown type for _commands property on table: {self._db_type_name()}")
