from typing import Annotated, Any

from pydantic import Discriminator, Tag

from .bar_chart import BarChart
from .base import BaseVisual
from .basic_shape import BasicShape
from .column_chart import ColumnChart
from .pie_chart import PieChart
from .slicer import Slicer
from .table import TableChart
from .text_box import TextBox


def get_visual(v: object | dict[str, Any]) -> str:
    if isinstance(v, dict):
        assert "visualType" in v
        assert isinstance(v["visualType"], str)

        mapping = {
            "barChart": "BarChart",
            "basicShape": "BasicShape",
            "columnChart": "ColumnChart",
            "pieChart": "PieChart",
            "slicer": "Slicer",
            "tableEx": "TableChart",
            "textbox": "TextBox",
        }
        return mapping.get(v["visualType"], "BaseVisual")
    return v.__class__.__name__


Visual = Annotated[
    Annotated[BarChart, Tag("BarChart")]
    | Annotated[BaseVisual, Tag("BaseVisual")]
    | Annotated[BasicShape, Tag("BasicShape")]
    | Annotated[ColumnChart, Tag("ColumnChart")]
    | Annotated[PieChart, Tag("PieChart")]
    | Annotated[Slicer, Tag("Slicer")]
    | Annotated[TableChart, Tag("TableChart")]
    | Annotated[TextBox, Tag("TextBox")],
    Discriminator(get_visual),
]


__all__ = ["BaseVisual", "Visual"]
