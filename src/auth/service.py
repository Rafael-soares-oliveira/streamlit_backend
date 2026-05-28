import os
from dataclasses import dataclass

import streamlit as st
import streamlit_authenticator as stauth

from config.settings import Settings


@dataclass(frozen=True)
class AuthenticatedUser:
    name: str
    username: str
    role: str


def _credentials_from_secrets() -> dict:
    auth_section = st.secrets.get("auth", {})
    if auth_section is None:
        return {}

    return auth_section.get("credentials", {})


def _fallback_credentials() -> dict:
    return {
        "usernames": {
            "admin": {
                "name": "Administrator",
                "email": "admin@example.com",
                "password": os.getenv("APP_ADMIN_PASSWORD_HASH", ""),
                "role": "admin",
            },
            "user": {
                "name": "Business User",
                "email": "user@example.com",
                "password": os.getenv("APP_USER_PASSWORD_HASH", ""),
                "role": "user",
            },
        }
    }


def get_authenticator(settings: Settings) -> stauth.Authenticate:
    credentials = _credentials_from_secrets() or _fallback_credentials()
    return stauth.Authenticate(
        credentials=credentials,
        cookie_name=settings.auth_cookie_name,
        cookie_key=settings.auth_cookie_key,
        cookie_expiry_days=settings.auth_cookie_expiry_days,
    )


def login(
    authenticator: stauth.Authenticate, credentials: dict
) -> AuthenticatedUser | None:
    # 1. Executa o login (renderiza o formulário ou valida o cookie)
    authenticator.login(key="Login", location="main")

    # 2. O streamlit-authenticator salva o status atual no st.session_state
    auth_status = st.session_state.get("authentication_status")
    username = st.session_state.get("username")
    name = st.session_state.get("name")

    # 3. Trata os três cenários possíveis de autenticação
    if auth_status is False:
        st.error("Usuário ou senha inválidos.")
        return None

    if auth_status is None:
        st.warning("Informe suas credenciais para continuar.")
        return None

    # 4. Se auth_status for True, busca a role e retorna o usuário instanciando
    if auth_status is True and username and name:
        users = credentials.get("usernames", {})
        role = users.get(username, {}).get("role", "user")
        return AuthenticatedUser(name=name, username=username, role=role)

    return None


def can_access_admin(user: AuthenticatedUser) -> bool:
    return user.role.lower() == "admin"
