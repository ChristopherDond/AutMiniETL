from __future__ import annotations

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

from autminietl.config import SETTINGS

st.set_page_config(page_title="AutMiniETL Dashboard", layout="wide")
st.title("AutMiniETL Dashboard")

engine = create_engine(SETTINGS.database_url, future=True)

runs_df = pd.read_sql("SELECT * FROM etl_runs ORDER BY started_at DESC", con=engine)
versions_df = pd.read_sql("SELECT * FROM dataset_versions ORDER BY created_at DESC", con=engine)
records_df = pd.read_sql("SELECT * FROM records", con=engine)

col1, col2, col3 = st.columns(3)
col1.metric("Runs", len(runs_df))
col2.metric("Versions", len(versions_df))
col3.metric("Records", len(records_df))

st.subheader("Recent runs")
st.dataframe(runs_df.head(20), use_container_width=True)

st.subheader("Version history")
st.dataframe(versions_df.head(20), use_container_width=True)

if not records_df.empty:
    st.subheader("Records by category")
    category_counts = records_df.groupby("category").size().rename("count")
    st.bar_chart(category_counts)

    st.subheader("Records by version")
    version_counts = records_df.groupby("version_id").size().rename("count")
    st.line_chart(version_counts)

    st.subheader("Records sample")
    st.dataframe(records_df.head(100), use_container_width=True)
else:
    st.info("No records yet. Run the ETL first using run_pipeline.py")
