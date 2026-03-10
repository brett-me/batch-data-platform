from __future__ import annotations

from pathlib import Path

STAGING_SQL_DIR = Path("sql/staging")


def get_stage_model_files() -> list[Path]:
    return sorted(STAGING_SQL_DIR.glob("*.sql"))


def get_view_name(model_file: Path) -> str:
    return model_file.stem


def build_stage_view_sql(view_name: str, model_sql: str) -> str:
    return f"""
    create or replace view staging.{view_name} as
    {model_sql.strip()}
    """.strip()