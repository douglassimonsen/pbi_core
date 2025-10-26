import json
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal, TypeVar

from pbi_core.attrs import BaseValidation, fields
from pbi_core.lineage import LineageNode

from .find import FindMixin
from .xpath import XPathMixin

if TYPE_CHECKING:
    from pbi_core.ssas.server import BaseTabularModel

LAYOUT_ENCODING = "utf-16-le"


T = TypeVar("T", bound="LayoutNode")


class LayoutNode(BaseValidation, XPathMixin, FindMixin):
    _name_field: str | None = None  # name of the field used to populate __repr__

    def __repr__(self) -> str:
        return json.dumps(self.serialize(), indent=2)

    @staticmethod
    def serialize_helper(value: Any) -> Any:
        """Helper function to serialize a value.

        We need to separate from the main function to handle cases where there is a list of
        dictionaries such as the visual container properties.
        """
        if hasattr(value, "serialize"):
            return value.serialize()
        if isinstance(value, list):
            return [LayoutNode.serialize_helper(val) for val in value]
        if isinstance(value, dict):
            return {key: LayoutNode.serialize_helper(val) for key, val in value.items()}
        if isinstance(value, Enum):
            return value.name
        return value

    def serialize(self) -> dict[str, Any]:
        """Serialize the node to a dictionary.

        Differs from the model_dump_json method in that it does not convert the JSON models back to strings.
        """
        ret = {}
        for field in fields(self.__class__):
            if field.init is False:
                continue
            ret[field.name] = self.serialize_helper(getattr(self, field.name))
        return ret

    def pbi_core_name(self) -> str:
        raise NotImplementedError

    def _children(self) -> list["LayoutNode"]:
        ret: list[LayoutNode] = []
        for attr in dir(self):
            if attr.startswith("_"):
                continue
            child_candidate: list[Any] | dict[str, Any] | LayoutNode | int | str = getattr(self, attr)
            if isinstance(child_candidate, list):
                ret.extend(val for val in child_candidate if isinstance(val, LayoutNode))
            elif isinstance(child_candidate, dict):
                ret.extend(val for val in child_candidate.values() if isinstance(val, LayoutNode))
            elif isinstance(child_candidate, LayoutNode):
                ret.append(child_candidate)
        return ret

    def get_lineage(
        self,
        lineage_type: Literal["children", "parents"],
        tabular_model: "BaseTabularModel",
    ) -> LineageNode:
        raise NotImplementedError
