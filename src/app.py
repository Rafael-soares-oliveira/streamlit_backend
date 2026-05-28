import streamlit as st

from auth import can_access_admin, get_authenticator, login
from auth.service import _credentials_from_secrets, _fallback_credentials
from config import ensure_duckdb_bootstrap, get_settings
from pages import admin, exploration, models_center
from telemetry import log_message_event


def main() -> None:
    settings = get_settings()
    ensure_duckdb_bootstrap(settings.duckdb_path)

    st.set_page_config(page_title=settings.app_title, layout="wide")
    st.title(settings.app_title)

    authenticator = get_authenticator(settings)
    credentials = _credentials_from_secrets() or _fallback_credentials()

    user = login(authenticator, credentials)

    if user is None:
        return

    log_message_event(
        settings.duckdb_path,
        level="info",
        component="auth",
        message="User login successful",
        user_name=user.username,
    )

    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Usuario: {user.name}")
    st.sidebar.write(f"Perfil: {user.role}")

    pages = {
        "Exploracao": exploration.render,
        "Modelos": models_center.render,
    }
    if can_access_admin(user):
        pages["Admin"] = admin.render

    selected_page = st.sidebar.radio("Navegacao", list(pages.keys()))
    pages[selected_page]()


if __name__ == "__main__":
    main()
