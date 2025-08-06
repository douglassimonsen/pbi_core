from typing import Annotated, Any, Union

from pydantic import Discriminator, Tag

from .bar_chart import BarChart
from .base import BaseVisual
from .column_chart import ColumnChart
from .pie_chart import PieChart
from .slicer import Slicer
from .table import TableChart


def get_visual(v: Any) -> str:
    if isinstance(v, dict):
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
        print(v["visualType"])
        breakpoint()
        return "BaseVisual"
    return v.__class__.__name__


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


__all__ = ["Visual"]
