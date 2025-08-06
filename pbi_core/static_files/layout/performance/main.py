from dataclasses import dataclass


@dataclass
class Performance:
    total_seconds: float
    rows_retrieved: int

    def __str__(self) -> str:
        return f"Performance(time={round(self.total_seconds, 2)}, rows={self.rows_retrieved})"
