from pydantic import ConfigDict

from pbi_core.static_files.layout._base_node import LayoutNode

from .base import BaseVisual
from .properties.base import Expression


class LabelsPropertiesHelper(LayoutNode):
    fontSize: Expression | None = None
    funnelLabelStyle: Expression | None = None
    labelDisplayUnits: Expression | None = None


class LabelsProperties(LayoutNode):
    properties: LabelsPropertiesHelper


class FunnelProperties(LayoutNode):
    labels: list[LabelsProperties] | None = None


class Funnel(BaseVisual):
    visualType: str = "funnel"
    model_config = ConfigDict(extra="forbid")

    drillFilterOtherVisuals: bool = True
    objects: FunnelProperties | None = None
