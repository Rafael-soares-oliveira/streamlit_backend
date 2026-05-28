from pathlib import Path

import duckdb

from src.config.database import ensure_duckdb_bootstrap
from src.config.settings import get_settings


def test_get_settings_uses_default_duckdb_path(monkeypatch) -> None:
    monkeypatch.delenv("DUCKDB_PATH", raising=False)
    settings = get_settings()
    assert settings.duckdb_path.name == "analytics.duckdb"


def test_ensure_duckdb_bootstrap_creates_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "analytics.duckdb"
    ensure_duckdb_bootstrap(db_path)

    connection = duckdb.connect(str(db_path))
    try:
        telemetry_exists = connection.execute(
            """
            SELECT COUNT(*) > 0
            FROM information_schema.tables
            WHERE table_schema = 'infra' AND table_name = 'telemetry_system'
            """
        ).fetchone()
        telemetry_exists: bool = telemetry_exists[0] if telemetry_exists else False
        message_exists = connection.execute(
            """
            SELECT COUNT(*) > 0
            FROM information_schema.tables
            WHERE table_schema = 'infra' AND table_name = 'message_system'
            """
        ).fetchone()
        message_exists: bool = message_exists[0] if message_exists else False
    finally:
        connection.close()

    assert telemetry_exists is True
    assert message_exists is True
