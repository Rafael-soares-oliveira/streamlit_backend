# 📦 Modern Data Stack in a Box - Analytics Platform

## 🎯 Visão Geral
Plataforma de analytics interna modular, flexível e segura. Este projeto fornece um backend padronizado para ingestão, segurança, telemetria automatizada e governança de dados. O Administrador tem total liberdade para realizar engenharia de dados e modelagem estatística focada no negócio, sem precisar gerenciar a infraestrutura subjacente.

## 🏗️ Arquitetura e Stack Tecnológica
* **Origem (Operacional):** PostgreSQL.
* **Ingestão (EL):** `dlt` (data load tool) automatiza a extração e carga, lidando com cargas incrementais (Upsert/Append) via `updated_at`.
* **Motor Analítico & Armazenamento:** DuckDB (Arquivo local `.duckdb` de altíssima performance).
* **Transformações:** Ibis framework. Permite modelagem de dados em Python que é traduzida nativamente para consultas SQL no DuckDB.
* **Frontend:** Streamlit.
* **Segurança:** `streamlit-authenticator` (RBAC, senhas em hash bcrypt).
* **Observabilidade:** Sistema de telemetria assíncrono via decoradores (`@telemetry`) isolado em tabelas DuckDB (`infra.telemetry_system` e `infra.message_system`).
* **Governança de ML:** Contratos de dados imutáveis via Dataclasses Python (`ModelResult`).

## 🚀 Como Desenvolver (Para Administradores)
O backend já cuida da infraestrutura. Para criar novos dashboards:
1. Extraia os dados usando o módulo `src/ingestion/`.
2. Transforme os dados usando Ibis em `src/transformations/`.
3. Valide seus modelos de ML importando os contratos em `src/ml_contracts/`.
4. Crie a interface visual na pasta `src/pages/` e adicione ao `app.py`.
