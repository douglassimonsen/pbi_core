import datetime
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Any

import jinja2

from pbi_core.ssas.server.server import BaseServer
from pbi_core.ssas.server.tabular_model.tabular_model import LocalTabularModel
from pbi_core.ssas.server.trace.trace_enums import TraceEvents

TRACE_DIR = Path(__file__).parent / "templates"
TRACE_TEMPLATES: dict[str, jinja2.Template] = {
    f.name: jinja2.Template(f.read_text()) for f in TRACE_DIR.iterdir() if f.is_file()
}


@dataclass
class Performance:
    total_seconds: float
    rows_retrieved: int

    def __str__(self) -> str:
        return f"Performance(time={round(self.total_seconds, 2)}, rows={self.rows_retrieved})"


class PerformanceTrace:
    def __init__(
        self,
        server: BaseServer,
        events: Iterable[TraceEvents] = (TraceEvents.COMMAND_END, TraceEvents.QUERY_END),
    ) -> None:
        self.events = events
        self.server = server
        next_day = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        trace_name = f"pbi_core_{next_day.replace(':', '_')}"
        subscription_name = f"pbi_core_subscription_{next_day.replace(':', '_')}"
        self.trace_command = TRACE_TEMPLATES["trace.xml"].render(
            name=trace_name,
            stop_time=next_day,
            events=self.events,
        )
        self.subscribe_command = TRACE_TEMPLATES["subscribe.xml"].render(
            trace_name=trace_name,
            subscription_name=subscription_name,
        )

    def __enter__(self) -> "PerformanceTrace":
        self.server.query_xml(self.trace_command)
        self.server.query_xml(self.subscribe_command)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        pass

    def _gen_xml(self) -> str:
        pass

    def subscribe(self) -> None:
        pass


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
    with PerformanceTrace(model.server):
        func(model)
    return Performance(0, 0)
