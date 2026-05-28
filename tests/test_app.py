from unittest.mock import patch

import pytest
import streamlit as st

from src.app import main
from src.auth.service import AuthenticatedUser


@pytest.fixture(autouse=True)
def mock_app_dependencies():
    """Mocka todas as dependências globais e de infraestrutura do app."""
    with (
        patch("src.app.get_settings") as mock_settings,
        patch("src.app.ensure_duckdb_bootstrap") as mock_bootstrap,
        patch("src.app.log_message_event") as mock_log,
        patch("src.app.get_authenticator") as mock_auth_obj,
        patch("src.app._credentials_from_secrets", return_value={"usernames": {}}),
        patch("src.app._fallback_credentials", return_value={}),
        patch.object(st, "secrets", {}),
        patch.object(st, "set_page_config"),
        patch.object(st, "title"),
    ):
        # Configurações dummy para evitar erros de atributo
        mock_settings.return_value.duckdb_path = "dummy.db"
        mock_settings.return_value.app_title = "Test App"

        yield {
            "bootstrap": mock_bootstrap,
            "log": mock_log,
            "authenticator": mock_auth_obj.return_value,
        }


def test_main_user_not_authenticated() -> None:
    """Se o login retornar None, o app deve parar imediatamente."""
    with (
        patch("src.app.login", return_value=None) as mock_login,
        patch.object(st, "sidebar") as mock_sidebar,
    ):
        main()

        mock_login.assert_called_once()
        mock_sidebar.write.assert_not_called()  # Garante que não renderizou a UI


def test_main_user_login_regular_role() -> None:
    """Usuário comum não deve ver o menu Admin."""
    regular_user = AuthenticatedUser(name="User", username="user1", role="user")

    with (
        patch("src.app.login", return_value=regular_user),
        patch.object(st.sidebar, "radio", return_value="Exploracao") as mock_radio,
        patch.object(st.sidebar, "write"),
        patch(
            "src.pages.exploration.render"
        ) as mock_render,  # Evita executar o render real
    ):
        main()

        # O primeiro argumento posicional ([0]), na segunda posição ([1]), contém a lista de páginas
        called_pages = mock_radio.call_args[0][1]
        assert "Exploracao" in called_pages
        assert "Modelos" in called_pages
        assert "Admin" not in called_pages
        mock_render.assert_called_once()


def test_main_user_login_admin_role() -> None:
    """Administrador deve visualizar o menu Admin."""
    admin_user = AuthenticatedUser(name="Admin", username="admin1", role="admin")

    with (
        patch("src.app.login", return_value=admin_user),
        patch.object(st.sidebar, "radio", return_value="Admin") as mock_radio,
        patch.object(st.sidebar, "write"),
        patch("src.pages.admin.render") as mock_render,  # Evita executar o render real
    ):
        main()

        called_pages = mock_radio.call_args[0][1]
        assert "Admin" in called_pages
        mock_render.assert_called_once()
