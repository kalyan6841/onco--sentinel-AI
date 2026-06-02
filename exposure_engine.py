from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def build_exposure_summary(treatment_df: pd.DataFrame) -> pd.DataFrame:
    exposure = (
        treatment_df.groupby("Drug_Administered")
        .agg(
            Total_Cumulative_Dose_mg=("Dose_Given_mg", "sum"),
            Cycles_Completed=("Cycle_Number", "nunique"),
            First_Date=("Treatment_Date", "min"),
            Last_Date=("Treatment_Date", "max"),
        )
        .reset_index()
        .sort_values("Total_Cumulative_Dose_mg", ascending=False)
    )
    exposure["Exposure_Timeline_Days"] = (
        exposure["Last_Date"] - exposure["First_Date"]
    ).dt.days
    return exposure


def render_exposure_engine(treatment_df: pd.DataFrame) -> None:
    st.subheader("Cumulative Drug Exposure Engine")
    exposure = build_exposure_summary(treatment_df)
    st.dataframe(exposure, use_container_width=True, hide_index=True)

    line_data = treatment_df.copy()
    line_data["Running_Dose_mg"] = line_data.groupby("Drug_Administered")["Dose_Given_mg"].cumsum()
    trend = px.line(
        line_data,
        x="Treatment_Date",
        y="Running_Dose_mg",
        color="Drug_Administered",
        markers=True,
        title="Cumulative exposure over time",
    )
    trend.update_layout(height=450)
    st.plotly_chart(trend, use_container_width=True)
