from collections.abc import Callable
from typing import Any

from pbi_core.ssas.server.tabular_model.tabular_model import LocalTabularModel

from .performance_trace import Performance, PerformanceTrace


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
    perf_trace = PerformanceTrace(model, [lambda: func(model)])
    return perf_trace.get_performance()[1]
