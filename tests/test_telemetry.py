from pathlib import Path

import duckdb

from src.config.database import ensure_duckdb_bootstrap
from src.telemetry import TelemetryEvent, log_message_event, log_telemetry_event


def test_log_events_insert_rows(tmp_path: Path) -> None:
    db_path = tmp_path / "analytics.duckdb"
    ensure_duckdb_bootstrap(db_path)

    log_telemetry_event(
        db_path,
        TelemetryEvent(
            component="tests",
            func_name="test_log_events_insert_rows",
            status="SUCCESS",
            duration_ms=12.0,
        ),
    )
    log_message_event(
        db_path,
        level="info",
        component="tests",
        message="ok",
    )

    connection = duckdb.connect(str(db_path))
    try:
        telemetry_count = connection.execute(
            "SELECT COUNT(*) FROM infra.telemetry_system"
        ).fetchone()

        telemetry_count: int = telemetry_count[0] if telemetry_count else 0

        message_count = connection.execute(
            "SELECT COUNT(*) FROM infra.message_system"
        ).fetchone()
        message_count: int = message_count[0] if message_count else 0
    finally:
        connection.close()

    assert telemetry_count == 1
    assert message_count == 1
