from typing import Annotated, Any, Union, cast

from pydantic import Discriminator, Tag

from .bar_chart import BarChart
from .base import BaseVisual
from .basic_shape import BasicShape
from .column_chart import ColumnChart
from .pie_chart import PieChart
from .slicer import Slicer
from .table import TableChart
from .text_box import TextBox


def get_visual(v: Any) -> str:
    if isinstance(v, dict):
        assert "visualType" in v
        assert isinstance(v["visualType"], str)
        # textbox
        match v["visualType"]:
            case "barChart":
                return "BarChart"
            case "basicShape":
                return "BasicShape"
            case "columnChart":
                return "ColumnChart"
            case "pieChart":
                return "PieChart"
            case "tableEx":
                return "TableChart"
            case "slicer":
                return "Slicer"
            case "textbox":
                return "TextBox"
            case _:
                return "BaseVisual"
    return cast(str, v.__class__.__name__)  # type: ignore


Visual = Annotated[
    Union[
        Annotated[BarChart, Tag("BarChart")],
        Annotated[BaseVisual, Tag("BaseVisual")],
        Annotated[BasicShape, Tag("BasicShape")],
        Annotated[ColumnChart, Tag("ColumnChart")],
        Annotated[PieChart, Tag("PieChart")],
        Annotated[Slicer, Tag("Slicer")],
        Annotated[TableChart, Tag("TableChart")],
        Annotated[TextBox, Tag("TextBox")],
    ],
    Discriminator(get_visual),
]


__all__ = ["BaseVisual", "Visual"]
