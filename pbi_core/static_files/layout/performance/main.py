import datetime
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Any

import jinja2

from pbi_core.ssas.server.tabular_model.tabular_model import BaseTabularModel, LocalTabularModel
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
    # TODO: create a subthread that runs the subscribe on a separate thread, collecting the records (+n second delay?), saving to a thread-safe list. Once the commands have been run, run the delete trace on main thread + close conn on secondary thread. Return all trace records
    def __init__(
        self,
        db: BaseTabularModel,
        events: Iterable[TraceEvents] = (TraceEvents.COMMAND_END, TraceEvents.QUERY_END),
    ) -> None:
        self.events = events
        self.db: BaseTabularModel = db
        self.conn = self.db.server.conn(db_name=self.db.db_name).open()
        next_day = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        trace_name = f"pbi_core_{next_day.replace(':', '_')}"
        subscription_name = f"pbi_core_subscription_{next_day.replace(':', '_')}"
        self.trace_create_command = TRACE_TEMPLATES["trace_create.xml"].render(
            trace_name=trace_name,
            stop_time=next_day,
            events=self.events,
        )
        self.subscription_create_command = TRACE_TEMPLATES["subscription_create.xml"].render(
            trace_name=trace_name,
            subscription_name=subscription_name,
        )
        self.trace_delete_command = TRACE_TEMPLATES["trace_delete.xml"].render(
            trace_name=trace_name,
        )

    def __enter__(self) -> "PerformanceTrace":
        self.db.server.query_xml(self.trace_create_command)
        self.cursor = self.conn.cursor()
        self.cursor.execute_dax(self.subscription_create_command)
        return self

    def get_performance(self) -> Iterator[tuple[Any, ...]]:
        while True:
            yield next(self.cursor.fetchone())

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        print("Exiting")
        with self.db.server.conn(db_name=self.db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute_xml(self.trace_delete_command)


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
