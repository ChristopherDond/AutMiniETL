from __future__ import annotations

import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    for col in ["title", "body"]:
        cleaned[col] = (
            cleaned[col]
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    cleaned = cleaned[cleaned["title"].str.len() > 0]
    cleaned = cleaned[cleaned["body"].str.len() > 0]

    cleaned["value"] = cleaned["body"].str.len().astype(float)
    cleaned["category"] = pd.cut(
        cleaned["value"],
        bins=[-1, 60, 130, 10_000],
        labels=["small", "medium", "large"],
    ).astype(str)

    cleaned = cleaned[[
        "external_id",
        "title",
        "body",
        "value",
        "category",
        "collected_at",
        "source_url",
    ]]

    return cleaned.reset_index(drop=True)
