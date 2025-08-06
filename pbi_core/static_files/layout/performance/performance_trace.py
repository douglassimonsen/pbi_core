import datetime
import threading
import time
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jinja2
from pyadomd import Pyadomd

from pbi_core.ssas.server.tabular_model.tabular_model import BaseTabularModel
from pbi_core.ssas.server.trace.trace_enums import TraceEvents

TRACE_DIR = Path(__file__).parent / "templates"
TRACE_TEMPLATES: dict[str, jinja2.Template] = {
    f.name: jinja2.Template(f.read_text()) for f in TRACE_DIR.iterdir() if f.is_file()
}


@dataclass
class ThreadResult:
    command: str
    rows_returned: int

    def get_performance(self, trace_records: list[dict[str, Any]]) -> "Performance":
        for record in trace_records:
            if record.get("TextData") == self.command:
                return Performance(
                    command_text=record["TextData"],
                    start_datetime=record["StartTime"],
                    end_datetime=record["EndTime"],
                    cpu_time=record["CPUTime"],
                    duration=record["Duration"],
                    rows_returned=self.rows_returned,
                )
        msg = f"Command '{self.command}' not found in trace records."
        raise ValueError(msg)


@dataclass
class Performance:
    command_text: str
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    cpu_time: int
    # duration is the total time in milliseconds
    duration: int
    rows_returned: int

    def __repr__(self) -> str:
        cmd: str = self.command_text[:100].replace("\n", "\\n")
        duration = round(self.duration / 1000, 2)
        cpu_time = round(self.cpu_time / 1000, 2)
        return f"Performance(duration={duration}, cpu_time={cpu_time}, rows={self.rows_returned}, command={cmd})"


class Subscriber:
    trace_records: list[dict[str, Any]]

    def __init__(self, subscription_create_command: str, conn: Pyadomd, events: Iterable[TraceEvents]) -> None:
        self.cursor = conn.cursor()
        self.cursor.execute_dax(subscription_create_command)
        self.events = events
        self.trace_records = []
        self.thread = threading.Thread(target=self.poll_cursor, daemon=True)
        self.thread.start()

    def poll_cursor(self) -> None:
        event_mapping = {e.value: e.name for e in self.events}
        for record in self.cursor.fetch_stream():
            if "EventClass" in record:
                record["EventClass"] = event_mapping[record["EventClass"]]
            self.trace_records.append(record)

    def kill_polling(self) -> None:
        if self.thread.is_alive():
            self.thread.join(timeout=1)

    def __repr__(self) -> str:
        return f"Subscriber(records={len(self.trace_records)})"


class PerformanceTrace:
    def __init__(
        self,
        db: BaseTabularModel,
        commands: list[str],
        events: Iterable[TraceEvents] = (TraceEvents.COMMAND_END, TraceEvents.QUERY_END),
    ) -> None:
        self.events = events
        self.db: BaseTabularModel = db
        self.commands = [x.replace("\r\n", "\n") for x in commands]

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

    def initialize_tracing(self) -> "PerformanceTrace":
        self.db.server.query_xml(self.trace_create_command)
        self.subscriber = Subscriber(
            self.subscription_create_command,
            self.get_conn(),
            self.events,
        )
        return self

    def terminate_tracing(self) -> None:
        with self.db.server.conn(db_name=self.db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute_xml(self.trace_delete_command)

    def get_performance(self) -> list[Performance]:
        def thread_func(command: str) -> ThreadResult:
            cursor = self.get_conn().cursor()
            cursor.execute_dax(command)
            rows_returned = len(cursor.fetch_all(limit=500))

            # See note in Cursor.fetch_stream() documentation for why we do this
            cursor._reader.Close()

            # The limit of 500 is to mimic the behavior of PowerBI, which returns by defult 500 rows
            return ThreadResult(
                command=command,
                rows_returned=rows_returned,
            )

        self.initialize_tracing()

        with ThreadPoolExecutor() as dax_executor:
            command_results = list(dax_executor.map(thread_func, self.commands))
        # TODO: better check for late records in trace

        missing_subscription_records = command_results
        for _ in range(15):
            # Testing for 5 seconds to check that all commands have an entry in the trace
            new_missing_subscription_records = [
                command
                for command in missing_subscription_records
                if not any(x.get("TextData") == command.command for x in self.subscriber.trace_records)
            ]

            if not new_missing_subscription_records:
                break
            time.sleep(1)
            missing_subscription_records = new_missing_subscription_records
        else:
            missing_commands = ", ".join(cmd.command for cmd in missing_subscription_records)
            msg = f"Some commands did not have trace records: {missing_commands}"
            raise ValueError(msg)

        self.subscriber.kill_polling()

        return [command_result.get_performance(self.subscriber.trace_records) for command_result in command_results]

    def get_conn(self) -> Pyadomd:
        return self.db.server.conn(db_name=self.db.db_name).open()
