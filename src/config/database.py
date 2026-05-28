from pathlib import Path

import duckdb


TELEMETRY_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS infra.telemetry_system (
    timestamp TIMESTAMP,
    correlation_id UUID,
    user_name VARCHAR,
    component VARCHAR,
    func_name VARCHAR,
    args_kwargs JSON,
    status VARCHAR,
    duration_ms DOUBLE,
    hw_metrics JSON,
    details JSON
);
"""

MESSAGE_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS infra.message_system (
    timestamp TIMESTAMP,
    level VARCHAR,
    correlation_id UUID,
    component VARCHAR,
    message VARCHAR,
    user_name VARCHAR,
    context JSON
);
"""


def ensure_duckdb_bootstrap(duckdb_path: Path) -> None:
    duckdb_path.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(duckdb_path))
    try:
        connection.execute("CREATE SCHEMA IF NOT EXISTS infra;")
        connection.execute(TELEMETRY_TABLE_DDL)
        connection.execute(MESSAGE_TABLE_DDL)
    finally:
        connection.close()
