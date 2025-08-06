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
    parent: "LayoutNode" = None

    def find_all(self, cls_type: type[T], attributes: Optional[dict[str, Any]] = None) -> list["T"]:
        attributes = attributes or {}
        ret: list["T"] = []
        if isinstance(self, cls_type) and all(
            getattr(self, field_name) == field_value for field_name, field_value in attributes.items()
        ):
            ret.append(self)
        for child in self._children():
            ret.extend(child.find_all(cls_type, attributes))
        return ret

    def find(self, cls_type: type[T], attributes: Optional[dict[str, Any]] = None) -> "T":
        attributes = attributes or {}
        if isinstance(self, cls_type) and all(
            getattr(self, field_name) == field_value for field_name, field_value in attributes.items()
        ):
            return self
        for child in self._children():
            try:
                return child.find(cls_type, attributes)
            except ValueError:
                pass
        raise ValueError(f"Object not found: {cls_type}")

    def next_sibling(self: T) -> T:
        raise NotImplementedError()

    def prev_sibling(self: T) -> T:
        raise NotImplementedError()

    def _children(self) -> list["LayoutNode"]:
        ret: list["LayoutNode"] = []
        for attr in dir(self):
            if attr == "parent" or attr.startswith("_"):
                continue
            child_candidate: Any = getattr(self, attr)
            if isinstance(child_candidate, list):
                for val in child_candidate:  # type: ignore
                    if isinstance(val, LayoutNode):
                        ret.append(val)
            elif isinstance(child_candidate, dict):
                for val in child_candidate.values():  # type: ignore
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

    def _set_parents(self) -> None:
        for field_name, field_type in self.model_fields.items():
            if not hasattr(field_type.annotation, "mro"):
                continue
            if any(typ is list for typ in field_type.annotation.mro()):
                for val in getattr(self, field_name):
                    if isinstance(val, LayoutNode):
                        val.parent = self
                        val._set_parents()
            elif any(typ is LayoutNode for typ in field_type.annotation.mro()) and field_name != "parent":
                val = getattr(self, field_name)
                val.parent = self
                val._set_parents()

    def get_xpath(self) -> list[str]:
        breakpoint()
