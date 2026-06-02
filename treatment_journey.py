from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_DIR = Path(__file__).resolve().parent / "sample_data"


@st.cache_data
def load_treatment_journey() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "treatment_journey.csv", parse_dates=["Treatment_Date"])
    return df.sort_values(["Treatment_Date", "Cycle_Number"]).reset_index(drop=True)


def render_treatment_journey(treatment_df: pd.DataFrame, patient_id: str | None = None) -> None:
    st.subheader("Oncology Treatment Journey")
    if patient_id:
        treatment_df = treatment_df[treatment_df["Patient_ID"] == patient_id].copy()
    st.dataframe(treatment_df, use_container_width=True, hide_index=True)

    st.markdown("### Cycle Timeline")
    timeline = px.scatter(
        treatment_df,
        x="Treatment_Date",
        y="Cycle_Number",
        color="Drug_Administered",
        size="Dose_Given_mg",
        hover_data=["Protocol", "Route", "Supportive_Care_Medications"],
        title="Treatment cycles across time",
    )
    timeline.update_layout(height=450, legend_title_text="Drug")
    st.plotly_chart(timeline, use_container_width=True)

    st.markdown("### Supportive Care Summary")
    supportive = (
        treatment_df.assign(
            Supportive=treatment_df["Supportive_Care_Medications"].fillna("").str.split(";")
        )
        .explode("Supportive")
        .assign(Supportive=lambda frame: frame["Supportive"].str.strip())
    )
    supportive = (
        supportive[supportive["Supportive"] != ""]
        .groupby("Supportive")["Cycle_Number"]
        .count()
        .reset_index(name="Occurrences")
        .sort_values("Occurrences", ascending=False)
    )
    st.dataframe(supportive, use_container_width=True, hide_index=True)
