from __future__ import annotations

from pathlib import Path

import pandas as pd

from autminietl.config import SETTINGS


def generate_reports(df: pd.DataFrame, run_id: str, source: str) -> tuple[Path, Path]:
    reports_dir = Path(SETTINGS.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    csv_path = reports_dir / f"dataset_{run_id}.csv"
    txt_path = reports_dir / f"summary_{run_id}.txt"

    df.to_csv(csv_path, index=False)

    summary = [
        f"run_id: {run_id}",
        f"source: {source}",
        f"rows: {len(df)}",
        f"mean_value: {df['value'].mean():.2f}",
        f"min_value: {df['value'].min():.2f}",
        f"max_value: {df['value'].max():.2f}",
        "category_counts:",
    ]
    for category, count in df["category"].value_counts().items():
        summary.append(f"- {category}: {count}")

    txt_path.write_text("\n".join(summary), encoding="utf-8")
    return csv_path, txt_path
