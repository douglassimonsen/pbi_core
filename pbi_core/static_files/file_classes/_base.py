import pydantic

MODEL_CONFIG = pydantic.ConfigDict(
    extra="forbid",
    use_enum_values=False,
    json_schema_mode_override="serialization",
    validate_assignment=True,
)


class BaseFileModel(pydantic.BaseModel):
    model_config = MODEL_CONFIG
