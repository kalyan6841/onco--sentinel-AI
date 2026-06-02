from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_DIR = Path(__file__).resolve().parent / "sample_data"


def classify_toxicity(lab_df: pd.DataFrame) -> pd.DataFrame:
    df = lab_df.copy()
    df["Hematologic_Risk"] = df["WBC_10e9_L"].apply(lambda v: "Elevated" if v < 3.0 else "Stable")
    df["Hepatic_Risk"] = df["Bilirubin_mg_dL"].apply(lambda v: "Elevated" if v > 1.2 else "Stable")
    df["Renal_Risk"] = df["Creatinine_mg_dL"].apply(lambda v: "Elevated" if v > 1.5 else "Stable")
    df["Electrolyte_Risk"] = df["Potassium_mmol_L"].apply(lambda v: "Elevated" if v < 3.5 else "Stable")
    return df


def render_toxicity_engine(patient: pd.Series, treatment_df: pd.DataFrame) -> None:
    st.subheader("Toxicity Intelligence Module")
    labs = pd.read_csv(DATA_DIR / "labs.csv", parse_dates=["Lab_Date"])
    labs = labs[labs["Patient_ID"] == patient["Patient_ID"]].copy()
    classified = classify_toxicity(labs)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hematologic flags", int((classified["Hematologic_Risk"] == "Elevated").sum()))
    c2.metric("Hepatic flags", int((classified["Hepatic_Risk"] == "Elevated").sum()))
    c3.metric("Renal flags", int((classified["Renal_Risk"] == "Elevated").sum()))
    c4.metric("Electrolyte flags", int((classified["Electrolyte_Risk"] == "Elevated").sum()))

    st.markdown("### Laboratory Trend Visualization")
    fig = px.line(
        classified,
        x="Lab_Date",
        y=["WBC_10e9_L", "Hemoglobin_g_dL", "Creatinine_mg_dL", "Bilirubin_mg_dL"],
        markers=True,
        title="Toxicity trend dashboard",
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Safety Monitoring Summary")
    st.dataframe(
        classified[
            ["Lab_Date", "WBC_10e9_L", "Hemoglobin_g_dL", "Creatinine_mg_dL", "Bilirubin_mg_dL", "Potassium_mmol_L"]
        ],
        use_container_width=True,
        hide_index=True,
    )
