from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


DATA_DIR = Path(__file__).resolve().parent / "sample_data"


def calculate_bsa(height_cm: float, weight_kg: float) -> float:
    return ((height_cm * weight_kg) / 3600.0) ** 0.5


@st.cache_data
def load_patient_profiles() -> pd.DataFrame:
    profiles = pd.read_csv(DATA_DIR / "patient_profile.csv")
    profiles["BSA"] = profiles.apply(
        lambda row: round(calculate_bsa(row["Height_cm"], row["Weight_kg"]), 2), axis=1
    )
    return profiles


def _metric_card(label: str, value: str) -> None:
    st.metric(label, value)


def render_patient_summary(patient: pd.Series) -> None:
    st.subheader("Patient Baseline Profile")
    left, right, center = st.columns([1.2, 1.2, 1.2])
    with left:
        _metric_card("Patient ID", str(patient["Patient_ID"]))
        _metric_card("Age", f"{int(patient['Age'])} years")
        _metric_card("Sex", str(patient["Sex"]))
        _metric_card("Height", f"{patient['Height_cm']} cm")
    with right:
        _metric_card("Weight", f"{patient['Weight_kg']} kg")
        _metric_card("BSA", f"{patient['BSA']} m²")
        _metric_card("Cancer Diagnosis", str(patient["Cancer_Diagnosis"]))
        _metric_card("Disease Stage", str(patient["Disease_Stage"]))
    with center:
        _metric_card("ECOG", str(patient["ECOG"]))
        _metric_card("Serum Creatinine", f"{patient['Serum_Creatinine_mg_dL']} mg/dL")
        _metric_card("AST", f"{patient['AST_U_L']} U/L")
        _metric_card("ALT", f"{patient['ALT_U_L']} U/L")

    st.markdown("### Baseline Laboratory Snapshot")
    lab_df = pd.DataFrame(
        {
            "Marker": ["CBC", "Creatinine", "AST", "ALT", "Bilirubin"],
            "Value": [
                patient["Baseline_CBC"],
                patient["Serum_Creatinine_mg_dL"],
                patient["AST_U_L"],
                patient["ALT_U_L"],
                patient["Bilirubin_mg_dL"],
            ],
        }
    )
    st.dataframe(lab_df, use_container_width=True, hide_index=True)

    st.markdown("### Patient Summary Dashboard")
    summary_fig = go.Figure()
    summary_fig.add_trace(
        go.Indicator(
            mode="number",
            value=float(patient["BSA"]),
            title={"text": "Body Surface Area (m²)"},
            domain={"x": [0, 0.5], "y": [0, 1]},
        )
    )
    summary_fig.add_trace(
        go.Indicator(
            mode="number",
            value=float(patient["Age"]),
            title={"text": "Age (years)"},
            domain={"x": [0.5, 1], "y": [0, 1]},
        )
    )
    summary_fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(summary_fig, use_container_width=True)
