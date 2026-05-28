from unittest.mock import MagicMock, patch

import pytest
import streamlit as st

from src.auth.service import (
    AuthenticatedUser,
    _credentials_from_secrets,
    _fallback_credentials,
    can_access_admin,
    get_authenticator,
    login,
)
from src.config.settings import Settings


def test_can_access_admin_true_for_admin_role() -> None:
    user = AuthenticatedUser(name="Administrator", username="admin", role="admin")
    assert can_access_admin(user) is True


def test_can_access_admin_false_for_user_role() -> None:
    user = AuthenticatedUser(name="Business User", username="user", role="user")
    assert can_access_admin(user) is False


# Testes de Credenciais e Configurações
def test_credentials_from_secrets_sucess() -> None:
    mock_secrets = {"auth": {"credentials": {"usernames": {"test": "pass"}}}}
    with patch.object(st, "secrets", mock_secrets):
        result = _credentials_from_secrets()
        assert result == {"usernames": {"test": "pass"}}


def test_credentials_from_secrets_empty() -> None:
    with patch.object(st, "secrets", {}):
        result = _credentials_from_secrets()
        assert result == {}


@patch.dict(
    "os.environ",
    {"APP_ADMIN_PASSWORD_HASH": "admin_hash", "APP_USER_PASSWORD_HASH": "user_hash"},
)
def test_fallback_credentials() -> None:
    credentials = _fallback_credentials()
    assert credentials["usernames"]["admin"]["password"] == "admin_hash"  # noqa: S105
    assert credentials["usernames"]["user"]["password"] == "user_hash"  # noqa: S105


@patch("src.auth.service._credentials_from_secrets")
@patch("src.auth.service.stauth.Authenticate")
def test_get_authenticator(
    mock_authenticate: MagicMock, mock_from_secrets: MagicMock
) -> None:
    mock_from_secrets.return_value = {"usernames": {"mock_user": {}}}
    mock_settings = MagicMock(spec=Settings)
    mock_settings.auth_cookie_name = "cookie"
    mock_settings.auth_cookie_key = "key"
    mock_settings.auth_cookie_expiry_days = 30

    with patch.object(st, "secrets", {}):
        get_authenticator(mock_settings)

    mock_authenticate.assert_called_once_with(
        credentials={"usernames": {"mock_user": {}}},
        cookie_name="cookie",
        cookie_key="key",
        cookie_expiry_days=30,
    )


# Testes da Função Login (Cenários do if/else)
@pytest.fixture
def mock_authenticator() -> MagicMock:
    return MagicMock()


@pytest.fixture
def sample_credentials() -> dict:
    return {
        "usernames": {
            "johndoe": {"name": "John", "role": "user"},
            "admin": {"name": "Admin", "role": "admin"},
        }
    }


def test_login_failed_status_false(
    mock_authenticator: MagicMock, sample_credentials: dict
) -> None:
    mock_session = {"authentication_status": False, "username": None, "name": None}

    with (
        patch.object(st, "session_state", mock_session),
        patch.object(st, "error") as mock_error,
    ):
        result = login(mock_authenticator, sample_credentials)

        assert result is None
        mock_error.assert_called_once_with("Usuário ou senha inválidos.")
        mock_authenticator.login.assert_called_once_with(key="Login", location="main")


def test_login_pending_status_none(
    mock_authenticator: MagicMock, sample_credentials: dict
) -> None:
    mock_session = {"authentication_status": None, "username": None, "name": None}

    with (
        patch.object(st, "session_state", mock_session),
        patch.object(st, "warning") as mock_warning,
    ):
        result = login(mock_authenticator, sample_credentials)

        assert result is None
        mock_warning.assert_called_once_with("Informe suas credenciais para continuar.")


def test_login_success_with_custom_role(
    mock_authenticator: MagicMock, sample_credentials: dict
) -> None:
    mock_session = {
        "authentication_status": True,
        "username": "admin",
        "name": "Admin",
    }

    with patch.object(st, "session_state", mock_session):
        result = login(mock_authenticator, sample_credentials)

    assert result == AuthenticatedUser(name="Admin", username="admin", role="admin")


def test_login_success_fallback_role(mock_authenticator: MagicMock) -> None:
    mock_session = {
        "authentication_status": True,
        "username": "johndoe",
        "name": "John",
    }

    empty_credentials = {
        "usernames": {}
    }  # Corrigido chave de 'username' para 'usernames' para bater com o service
    with patch.object(st, "session_state", mock_session):
        result = login(mock_authenticator, empty_credentials)

    assert result == AuthenticatedUser(name="John", username="johndoe", role="user")


def test_login_status_true_but_missing_data(
    mock_authenticator: MagicMock, sample_credentials: dict
) -> None:
    mock_session = {"authentication_status": True, "username": None, "name": "John"}

    with (
        patch.object(st, "secrets", {}),
        patch.object(st, "session_state", mock_session),
    ):
        result = login(mock_authenticator, sample_credentials)
        assert result is None
