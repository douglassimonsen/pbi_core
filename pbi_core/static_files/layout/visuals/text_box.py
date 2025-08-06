# ruff: noqa: N815
from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode

if TYPE_CHECKING:
    from pbi_core.static_files.model_references import ModelColumnReference, ModelMeasureReference


# TODO: remove Anys
class TextBox(LayoutNode):
    visualType: str = "textbox"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: Any
    vcObjects: Any = None
    display: Any = None

    def get_ssas_elements(self) -> "set[ModelColumnReference | ModelMeasureReference]":  # noqa: PLR6301
        return set()
