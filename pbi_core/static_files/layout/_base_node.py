from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar

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
    _parent: "LayoutNode"
    _xpath: list[str | int]

    def find_all(
        self, cls_type: type[T], attributes: Optional[dict[str, Any] | Callable[[T], bool]] = None
    ) -> list["T"]:
        ret: list["T"] = []
        if attributes is None:
            attribute_lambda: Callable[[T], bool] = lambda x: True  # noqa: E731
        elif isinstance(attributes, dict):
            attribute_lambda = lambda x: all(  # noqa: E731
                getattr(x, field_name) == field_value for field_name, field_value in attributes.items()
            )
        else:
            attribute_lambda = attributes
        if isinstance(self, cls_type) and attribute_lambda(self):
            ret.append(self)
        for child in self._children():
            ret.extend(child.find_all(cls_type, attributes))
        return ret

    def find(self, cls_type: type[T], attributes: Optional[dict[str, Any] | Callable[[T], bool]] = None) -> "T":
        if attributes is None:
            attribute_lambda: Callable[[T], bool] = lambda x: True  # noqa: E731
        elif isinstance(attributes, dict):
            attribute_lambda = lambda x: all(  # noqa: E731
                getattr(x, field_name) == field_value for field_name, field_value in attributes.items()
            )
        else:
            attribute_lambda = attributes
        if isinstance(self, cls_type) and attribute_lambda(self):
            return self
        for child in self._children():
            try:
                return child.find(cls_type, attributes)
            except ValueError:
                pass
        raise ValueError(f"Object not found: {cls_type}")

    def model_dump_json(self, **kwargs: Any):
        return super().model_dump_json(round_trip=True, exclude_unset=True, **kwargs)

    def next_sibling(self: T) -> T:
        raise NotImplementedError()

    def prev_sibling(self: T) -> T:
        raise NotImplementedError()

    def _children(self) -> list["LayoutNode"]:
        ret: list["LayoutNode"] = []
        for attr in dir(self):
            if attr.startswith("_"):
                continue
            child_candidate: list[Any] | dict[str, Any] | LayoutNode | int | str = getattr(self, attr)
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

    def find_xpath(self, xpath: list[str | int]) -> "LayoutNode":
        return _find_xpath(self, xpath)


def _find_xpath(val: LayoutNode | list[LayoutNode] | dict[str, LayoutNode] | str, xpath: list[str | int]) -> LayoutNode:
    if len(xpath) == 0:
        assert isinstance(val, LayoutNode)
        return val
    elif isinstance(val, list):
        next_pos = xpath.pop(0)
        assert isinstance(next_pos, int)
        return _find_xpath(val[next_pos], xpath)
    elif isinstance(val, dict):
        breakpoint()
    elif isinstance(val, LayoutNode):
        next_pos = xpath.pop(0)
        assert isinstance(next_pos, str)
        return _find_xpath(getattr(val, next_pos), xpath)
    raise ValueError(f"What? xpath={xpath}, val={val}")


def _set_parents(
    base: list[LayoutNode] | dict[str, LayoutNode] | LayoutNode | int | str,
    last_parent: "LayoutNode",
    curr_xpath: list[str | int],
) -> None:
    if isinstance(base, list):
        for i, val in enumerate(base):
            _set_parents(val, last_parent, curr_xpath + [i])
    elif isinstance(base, dict):
        for key, val in base.items():
            _set_parents(val, last_parent, curr_xpath + [key])
    elif isinstance(base, LayoutNode):
        base._parent = last_parent  # type: ignore
        base._xpath = curr_xpath  # type: ignore

        for field_name in base.model_fields.keys():
            if field_name.startswith("_"):
                continue
            field_value = getattr(base, field_name)
            if isinstance(field_value, (list, dict, LayoutNode)):
                _set_parents(field_value, base, curr_xpath + [field_name])  # type: ignore
