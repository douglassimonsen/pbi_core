from typing import Annotated, Any, Union, cast

from pydantic import Discriminator, Tag

from .bar_chart import BarChart
from .base import BaseVisual
from .column_chart import ColumnChart
from .pie_chart import PieChart
from .slicer import Slicer
from .table import TableChart


def get_visual(v: Any) -> str:
    if isinstance(v, dict):
        assert "visualType" in v
        assert isinstance(v["visualType"], str)
        match v["visualType"]:
            case "barChart":
                return "BarChart"
            case "columnChart":
                return "ColumnChart"
            case "pieChart":
                return "PieChart"
            case "tableEx":
                return "TableChart"
            case "slicer":
                return "Slicer"
            case _:
                "BaseVisual"
    return cast(str, v.__class__.__name__)  # type: ignore


Visual = Annotated[
    Union[
        Annotated[BarChart, Tag("BarChart")],
        Annotated[BaseVisual, Tag("BaseVisual")],
        Annotated[ColumnChart, Tag("ColumnChart")],
        Annotated[PieChart, Tag("PieChart")],
        Annotated[Slicer, Tag("Slicer")],
        Annotated[TableChart, Tag("TableChart")],
    ],
    Discriminator(get_visual),
]


__all__ = ["BaseVisual", "Visual"]
