from typing import Any, ClassVar, Self

from attrs import Attribute, field, fields, setters
from structlog import get_logger

from pbi_core.attrs import BaseValidation, define

logger = get_logger()


@define()
class SsasMixin(BaseValidation):
    id: int = field(eq=True, repr=True, on_setattr=setters.frozen)
    _db_field_names: ClassVar[dict[str, str]] = {}
    """Mapping of python attribute names to database field names.

    Example:
        For the Column class:
        {"ExplicitName": "explicit_name"...}
    """

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

    def get_altered_fields(self) -> list[Attribute]:
        """Returns a list of fields that have been altered since the last sync from SSAS."""
        ret = []
        for f in fields(self.__class__):
            if f.on_setattr is setters.frozen or f.name.startswith("_"):
                continue

            if self._original_data is None:
                ret.append(f)
                continue

            old_val = getattr(self._original_data, f.name, None)
            new_val = getattr(self, f.name)
            if old_val != new_val:
                ret.append(f)
        return ret

    def xml_fields(self) -> dict[str, Any]:
        base = self.model_dump()

        # All update/create commands require the ID field
        ret: dict[str, Any] = {
            "ID": self.id,
        }
        for f in self.get_altered_fields():
            db_name = self._db_field_names.get(f.name, f.name)
            ret[db_name] = base.get(f.name)
        return ret

    @classmethod
    def model_validate(cls, data: dict) -> Self:  # pyright: ignore[reportIncompatibleMethodOverride]
        formatted_data = cls.to_snake_case(data)

        return super().model_validate(formatted_data)
