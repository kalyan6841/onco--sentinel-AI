from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from exposure_engine import build_exposure_summary
from toxicity_engine import classify_toxicity


DATA_DIR = Path(__file__).resolve().parent / "sample_data"


def render_research_dashboard(patient: pd.Series, treatment_df: pd.DataFrame) -> None:
    st.subheader("Research Dashboard")
    labs = pd.read_csv(DATA_DIR / "labs.csv", parse_dates=["Lab_Date"])
    labs = labs[labs["Patient_ID"] == patient["Patient_ID"]].copy()
    tox = classify_toxicity(labs)
    exposure = build_exposure_summary(treatment_df)

    st.markdown("### Treatment Timeline")
    timeline = px.timeline(
        treatment_df.assign(End_Date=treatment_df["Treatment_Date"] + pd.Timedelta(days=1)),
        x_start="Treatment_Date",
        x_end="End_Date",
        y="Drug_Administered",
        color="Protocol",
        title="Treatment timeline",
    )
    timeline.update_layout(height=400)
    st.plotly_chart(timeline, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        exposure_fig = px.bar(
            exposure,
            x="Drug_Administered",
            y="Total_Cumulative_Dose_mg",
            title="Drug exposure timeline",
        )
        exposure_fig.update_layout(height=400)
        st.plotly_chart(exposure_fig, use_container_width=True)
    with col2:
        cycle_summary = treatment_df.groupby("Cycle_Number")["Dose_Given_mg"].sum().reset_index()
        cycle_fig = px.bar(cycle_summary, x="Cycle_Number", y="Dose_Given_mg", title="Cycle summary")
        cycle_fig.update_layout(height=400)
        st.plotly_chart(cycle_fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        tox_fig = px.line(
            tox,
            x="Lab_Date",
            y=["WBC_10e9_L", "Hemoglobin_g_dL", "Creatinine_mg_dL"],
            markers=True,
            title="Toxicity trends",
        )
        tox_fig.update_layout(height=400)
        st.plotly_chart(tox_fig, use_container_width=True)
    with col4:
        st.markdown("#### Safety Summary Snapshot")
        metric_cols = st.columns(2)
        metric_cols[0].metric("BSA", f"{float(patient['BSA']):.2f} m²")
        metric_cols[1].metric("Age", f"{int(patient['Age'])} years")
        st.caption("Educational snapshot for research and workflow context.")
