from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

import pandas as pd
import requests
from bs4 import BeautifulSoup

SourceName = Literal["mock", "api", "scrape"]


def _collect_mock() -> pd.DataFrame:
    now = datetime.now(timezone.utc)
    rows = [
        {"external_id": f"mock-{i}", "title": f"Sample {i}", "body": f"mock body text {i}", "source_url": None, "collected_at": now}
        for i in range(1, 21)
    ]
    return pd.DataFrame(rows)


def _collect_api() -> pd.DataFrame:
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    payload = response.json()
    now = datetime.now(timezone.utc)
    rows = [
        {
            "external_id": f"api-{item['id']}",
            "title": item["title"],
            "body": item["body"],
            "source_url": url,
            "collected_at": now,
        }
        for item in payload
    ]
    return pd.DataFrame(rows)


def _collect_scrape() -> pd.DataFrame:
    url = "https://quotes.toscrape.com/"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    quotes = soup.select(".quote")
    now = datetime.now(timezone.utc)
    rows = []
    for i, quote in enumerate(quotes, start=1):
        text = quote.select_one(".text").get_text(strip=True)
        author = quote.select_one(".author").get_text(strip=True)
        rows.append(
            {
                "external_id": f"scrape-{i}",
                "title": author,
                "body": text,
                "source_url": url,
                "collected_at": now,
            }
        )
    return pd.DataFrame(rows)


def collect(source: SourceName) -> pd.DataFrame:
    if source == "mock":
        return _collect_mock()
    if source == "api":
        return _collect_api()
    if source == "scrape":
        return _collect_scrape()
    raise ValueError(f"Unsupported source: {source}")
