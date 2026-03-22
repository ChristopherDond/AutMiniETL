from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import insert, update

from autminietl.collect import collect
from autminietl.db import etl_runs, get_engine, init_db
from autminietl.load import has_records_for_version, load_records, upsert_dataset_version
from autminietl.logger import configure_logging
from autminietl.report import generate_reports
from autminietl.transform import transform


def run_pipeline(source: str) -> dict:
    configure_logging()
    logger = logging.getLogger("autminietl.pipeline")
    engine = get_engine()
    init_db(engine)

    run_id = uuid4().hex[:12]
    started_at = datetime.now(timezone.utc)

    with engine.begin() as conn:
        conn.execute(
            insert(etl_runs).values(
                run_id=run_id,
                status="RUNNING",
                source=source,
                started_at=started_at,
            )
        )

    try:
        logger.info("Starting run=%s source=%s", run_id, source)
        raw_df = collect(source)
        transformed_df = transform(raw_df)
        version_id, is_new_version = upsert_dataset_version(engine, transformed_df, source)
        if is_new_version or not has_records_for_version(engine, version_id):
            rows_loaded = load_records(engine, transformed_df, version_id)
        else:
            rows_loaded = 0
            logger.info("Skipping load for existing version_id=%s (already loaded)", version_id)
        csv_path, summary_path = generate_reports(transformed_df, run_id, source)

        ended_at = datetime.now(timezone.utc)
        duration_seconds = (ended_at - started_at).total_seconds()

        with engine.begin() as conn:
            conn.execute(
                update(etl_runs)
                .where(etl_runs.c.run_id == run_id)
                .values(
                    status="SUCCESS",
                    ended_at=ended_at,
                    duration_seconds=duration_seconds,
                    rows_collected=len(raw_df),
                    rows_loaded=rows_loaded,
                    version_id=version_id,
                )
            )

        result = {
            "run_id": run_id,
            "status": "SUCCESS",
            "rows_collected": len(raw_df),
            "rows_loaded": rows_loaded,
            "version_id": version_id,
            "report_csv": str(csv_path),
            "report_summary": str(summary_path),
        }
        logger.info("Finished run=%s status=SUCCESS rows=%s", run_id, rows_loaded)
        return result

    except Exception as exc:
        ended_at = datetime.now(timezone.utc)
        duration_seconds = (ended_at - started_at).total_seconds()
        with engine.begin() as conn:
            conn.execute(
                update(etl_runs)
                .where(etl_runs.c.run_id == run_id)
                .values(
                    status="FAILED",
                    ended_at=ended_at,
                    duration_seconds=duration_seconds,
                    error_message=str(exc),
                )
            )
        logger.exception("Run failed run=%s", run_id)
        raise
