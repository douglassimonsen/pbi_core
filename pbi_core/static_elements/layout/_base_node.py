from typing import TYPE_CHECKING, Any, Optional, TypeVar

import pydantic

from ...lineage import LineageNode, LineageType

if TYPE_CHECKING:
    from ...ssas.server import BaseTabularModel

LAYOUT_ENCODING = "utf-16-le"

MODEL_CONFIG = pydantic.ConfigDict(
    extra="forbid",
    use_enum_values=False,
    json_schema_mode_override="serialization",
    validate_assignment=True,
)
T = TypeVar("T", bound="LayoutNode")


class LayoutNode(pydantic.BaseModel):
    model_config = MODEL_CONFIG
    _name_field: Optional[str] = None  # name of the field used to populate __repr__

    def find_all(self, cls_type: type[T], attributes: Optional[dict[str, Any]] = None) -> list["T"]:
        attributes = attributes or {}
        ret = []
        if isinstance(self, cls_type) and all(
            getattr(self, field_name) == field_value for field_name, field_value in attributes.items()
        ):
            ret.append(self)
        for child in self._children():
            if (candidates := child.find_all(cls_type, attributes)) is not None:
                ret.extend(candidates)
        return ret

    def find(self, cls_type: type[T], attributes: Optional[dict[str, Any]] = None) -> "T":
        attributes = attributes or {}
        if isinstance(self, cls_type) and all(
            getattr(self, field_name) == field_value for field_name, field_value in attributes.items()
        ):
            return self
        for child in self._children():
            if (candidate := child.find(cls_type, attributes)) is not None:
                return candidate
        raise ValueError(f"Object not found: {cls_type}")

    def next_sibling(self: T) -> T:
        raise NotImplementedError()

    def prev_sibling(self: T) -> T:
        raise NotImplementedError()

    def _children(self) -> list["LayoutNode"]:
        ret = []
        for attr in dir(self):
            if attr == "parent" or attr.startswith("_"):
                continue
            child_candidate = getattr(self, attr)
            if isinstance(child_candidate, list):
                for val in child_candidate:
                    if isinstance(val, LayoutNode):
                        ret.append(val)
            elif isinstance(child_candidate, dict):
                for val in child_candidate.values():
                    if isinstance(val, LayoutNode):
                        ret.append(val)
            elif isinstance(child_candidate, LayoutNode):
                ret.append(child_candidate)
        return ret

    def __str__(self) -> str:
        if self._name_field is None:
            return super().__str__()
        return f"{self.__class__.__name__}({getattr(self, self._name_field)})"

    def get_lineage(self, lineage_type: LineageType, tabular_model: "BaseTabularModel") -> LineageNode:
        raise NotImplementedError
