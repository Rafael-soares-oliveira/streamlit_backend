from typing import Any

import ibis


def register_source(connection_uri: str) -> Any:
    return ibis.duckdb.connect(connection_uri)
