import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import duckdb


@dataclass(frozen=True)
class TelemetryEvent:
    component: str
    func_name: str
    status: str
    duration_ms: float
    user_name: str = "anonymous"
    args_kwargs: dict | None = None
    hw_metrics: dict | None = None
    details: dict | None = None
    correlation_id: str | None = None


def _default_correlation_id(correlation_id: str | None) -> str:
    return correlation_id or str(uuid.uuid4())


def log_telemetry_event(duckdb_path: Path, event: TelemetryEvent) -> None:
    connection = duckdb.connect(str(duckdb_path))
    try:
        connection.execute(
            """
            INSERT INTO infra.telemetry_system (
                timestamp, correlation_id, user_name, component, func_name,
                args_kwargs, status, duration_ms, hw_metrics, details
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                datetime.now(UTC),
                _default_correlation_id(event.correlation_id),
                event.user_name,
                event.component,
                event.func_name,
                json.dumps(event.args_kwargs or {}),
                event.status,
                event.duration_ms,
                json.dumps(event.hw_metrics or {}),
                json.dumps(event.details or {}),
            ],
        )
    finally:
        connection.close()


def log_message_event(
    duckdb_path: Path,
    *,
    level: str,
    component: str,
    message: str,
    user_name: str = "anonymous",
    context: dict | None = None,
    correlation_id: str | None = None,
) -> None:
    connection = duckdb.connect(str(duckdb_path))
    try:
        connection.execute(
            """
            INSERT INTO infra.message_system (
                timestamp, level, correlation_id, component, message, user_name, context
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                datetime.now(UTC),
                level.upper(),
                _default_correlation_id(correlation_id),
                component,
                message,
                user_name,
                json.dumps(context or {}),
            ],
        )
    finally:
        connection.close()
