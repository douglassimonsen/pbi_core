from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, model_validator

if TYPE_CHECKING:
    pass


SsasConfig = ConfigDict(
    extra="forbid",
    use_enum_values=False,
    json_schema_mode_override="serialization",
    validate_assignment=True,
    protected_namespaces=(),
)


class SsasTable(BaseModel):  # type: ignore
    model_config = SsasConfig

    @classmethod
    def _db_type_name(cls) -> str:
        return cls.__name__

    @model_validator(mode="before")  # type: ignore
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
