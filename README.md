# AutMiniETL

AutMiniETL is a mini ETL platform in Python that:

- Collects data (API, scraping, or local mock)
- Transforms data with Pandas
- Loads data into SQLite (default) or PostgreSQL
- Generates automatic reports
- Keeps execution logs and dataset versions
- Offers a simple Streamlit dashboard

## Project structure

```
autminietl/
  __init__.py
  collect.py
  config.py
  db.py
  load.py
  logger.py
  pipeline.py
  report.py
  transform.py
run_pipeline.py
scheduler_app.py
dashboard.py
requirements.txt
.env.example
```

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
```

## Run once

```bash
python run_pipeline.py --source mock
```

Sources available: `mock`, `api`, `scrape`.

## Run scheduler

```bash
python scheduler_app.py
```

The scheduler executes using `DEFAULT_SOURCE` every `SCHEDULE_MINUTES`.

## Open dashboard

```bash
streamlit run dashboard.py
```

## Database

Default database URL:

```env
DATABASE_URL=sqlite:///data/autminietl.db
```

For PostgreSQL, set for example:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/autminietl
```

## Core tables

- `etl_runs`: execution logs (status, duration, errors)
- `dataset_versions`: dataset versions by content hash
- `records`: transformed records linked to a version
