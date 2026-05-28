# Modern Data Stack in a Box - Streamlit Backend

Versão atual: 0.0.0

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=Python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Docker-green?logo=Postgresql)](https://www.postgresql.org/)
[![Streamlit UI](https://img.shields.io/badge/Streamlit-Docker-green?logo=Streamlit)](https://docs.streamlit.io/)


[![CI](https://github.com/Rafael-soares-oliveira/ecommerce_mlops_genai_pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Rafael-soares-oliveira/ecommerce_mlops_genai_pipeline/actions/workflows/ci.yml)
![Coverage](./coverage.svg)

## Visao geral
Backend modular para analytics interno com foco em produtividade do Administrador. O projeto padroniza autenticação, bootstrap de DuckDB, telemetria e contratos de ML para que novos dashboards possam ser construidos sem reconstruir a infraestrutura.

## Stack
- Streamlit
- DuckDB
- Ibis
- dlt
- streamlit-authenticator
- pytest + ruff
- gerenciamento de ambiente com uv

## Estrutura atual
```text
streamlit_backend/
├── src/
│   ├── app.py
│   ├── auth/
│   ├── config/
│   ├── ml_contracts/
│   ├── pages/
│   ├── telemetry/
│   └── transformations/
├── tests/
├── .streamlit/
├── data/
├── pyproject.toml
└── README.md
```

## Como executar com uv
1. Instale dependencias:
   - `uv sync --dev`
2. Execute o app:
   - `uv run streamlit run src/app.py`
3. Rode lint:
   - `uv run ruff check .`
   - `uv run ruff format --check .`
4. Rode testes:
   - `uv run pytest`

## Autenticacao (MVP)
- O app usa `streamlit-authenticator`.
- Configure credenciais em `.streamlit/secrets.toml` sob a chave `auth.credentials`.
- Como fallback local, hashes podem ser lidos de:
  - `APP_ADMIN_PASSWORD_HASH`
  - `APP_USER_PASSWORD_HASH`

## DuckDB e telemetria
- O banco padrao e `data/analytics.duckdb`.
- O bootstrap cria automaticamente:
  - `infra.telemetry_system`
  - `infra.message_system`

## Contratos de ML
Contratos tipados em `src/ml_contracts/models.py`:
- `RegressionMetrics`
- `ClassificationMetrics`
- `ClusterMetrics`
- `ModelResult`

## Proximos passos sugeridos
- Corrigir página inicial.
- Melhorar sistema de Login.
- Implementar pipeline `dlt` incremental PostgreSQL -> DuckDB.
- Evoluir paginas de exploracao/modelos/admin.
- Adicionar masking de PII e buffer assincrono para telemetria.
