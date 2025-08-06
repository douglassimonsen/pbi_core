from typing import Any, Optional, TypeVar

import pydantic

T = TypeVar("T", bound="LayoutNode")


MODEL_CONFIG = pydantic.ConfigDict(
    extra="forbid",
    use_enum_values=False,
    json_schema_mode_override="serialization",
    validate_assignment=True,
)


class LayoutNode(pydantic.BaseModel):  # type: ignore
    _parent: "LayoutNode"

    def find_all(self, cls_type: type[T], attributes: Optional[dict[str, Any]] = None) -> list["T"]:
        attributes = attributes or {}
        ret = []
        if isinstance(self, cls_type) and all(
            getattr(self, field_name) == field_value for field_name, field_value in attributes.items()
        ):
            ret.append(self)
        for child in self.children:
            if (candidates := child.find_all(cls_type, attributes)) is not None:
                ret.extend(candidates)
        return ret

    def find(self, cls_type: type[T], attributes: Optional[dict[str, Any]] = None) -> "T":
        attributes = attributes or {}
        if isinstance(self, cls_type) and all(
            getattr(self, field_name) == field_value for field_name, field_value in attributes.items()
        ):
            return self
        for child in self.children:
            if (candidate := child.find(cls_type, attributes)) is not None:
                return candidate
        raise ValueError(f"Object not found: {cls_type}")

    def next_sibling(self: T) -> T:
        raise NotImplementedError()

    def prev_sibling(self: T) -> T:
        raise NotImplementedError()

    @property
    def children(self) -> list["LayoutNode"]:
        raise NotImplementedError()
