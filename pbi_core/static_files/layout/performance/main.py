from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pbi_core.ssas.server.tabular_model.tabular_model import LocalTabularModel

from .performance_trace import PerformanceTrace


@dataclass
class Performance:
    total_seconds: float
    rows_retrieved: int

    def __str__(self) -> str:
        return f"Performance(time={round(self.total_seconds, 2)}, rows={self.rows_retrieved})"


def get_performance(model: LocalTabularModel, func: Callable[[LocalTabularModel], Any]) -> Performance:
    """Calculates performance of a DAX query using a Trace.

    Args:
    ----
        func (Callable[[LocalTabularModel], Any]): a function that runs a DAX query on the SSAS instance.
            Takes a single argument: the SSAS instance the DAX should be run against
        model (LocalTabularModel): the SSAS instance the DAX should be run against

    Returns:
    -------
        Performance: contains memory and time usage of the DAX query


    """
    with PerformanceTrace(model) as perf_trace:
        func(model)
        perf = perf_trace.get_performance()
    print(next(perf))
    return Performance(0, 0)
