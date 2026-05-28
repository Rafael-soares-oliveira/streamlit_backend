import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    environment: str
    app_title: str
    data_dir: Path
    duckdb_path: Path
    auth_cookie_name: str
    auth_cookie_key: str
    auth_cookie_expiry_days: int


def get_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "data"
    return Settings(
        environment=os.getenv("APP_ENV", "development"),
        app_title=os.getenv("APP_TITLE", "Streamlit Backend"),
        data_dir=data_dir,
        duckdb_path=Path(os.getenv("DUCKDB_PATH", data_dir / "analytics.duckdb")),
        auth_cookie_name=os.getenv("AUTH_COOKIE_NAME", "streamlit_backend_auth"),
        auth_cookie_key=os.getenv("AUTH_COOKIE_KEY", "please-change-me"),
        auth_cookie_expiry_days=int(os.getenv("AUTH_COOKIE_EXPIRY_DAYS", "14")),
    )
