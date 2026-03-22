from __future__ import annotations

from pathlib import Path

from sqlalchemy import DateTime, Float, ForeignKey, Integer, MetaData, String, Table, Text, create_engine, Column
from sqlalchemy.engine import Engine

from autminietl.config import SETTINGS

metadata = MetaData()

etl_runs = Table(
    "etl_runs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("run_id", String(64), nullable=False, unique=True),
    Column("status", String(32), nullable=False),
    Column("source", String(32), nullable=False),
    Column("started_at", DateTime, nullable=False),
    Column("ended_at", DateTime, nullable=True),
    Column("duration_seconds", Float, nullable=True),
    Column("rows_collected", Integer, nullable=True),
    Column("rows_loaded", Integer, nullable=True),
    Column("version_id", Integer, nullable=True),
    Column("error_message", Text, nullable=True),
)

dataset_versions = Table(
    "dataset_versions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("version_hash", String(64), nullable=False, unique=True),
    Column("created_at", DateTime, nullable=False),
    Column("source", String(32), nullable=False),
    Column("row_count", Integer, nullable=False),
    Column("notes", Text, nullable=True),
)

records = Table(
    "records",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("version_id", Integer, ForeignKey("dataset_versions.id"), nullable=False),
    Column("external_id", String(64), nullable=False),
    Column("title", Text, nullable=False),
    Column("body", Text, nullable=False),
    Column("value", Float, nullable=False),
    Column("category", String(32), nullable=False),
    Column("collected_at", DateTime, nullable=False),
    Column("source_url", Text, nullable=True),
)


def _ensure_sqlite_path(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return
    db_path = database_url.replace("sqlite:///", "", 1)
    parent = Path(db_path).resolve().parent
    parent.mkdir(parents=True, exist_ok=True)


def get_engine() -> Engine:
    _ensure_sqlite_path(SETTINGS.database_url)
    return create_engine(SETTINGS.database_url, future=True)


def init_db(engine: Engine) -> None:
    metadata.create_all(engine)
