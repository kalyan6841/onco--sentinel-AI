from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st


def simulate_population_pk(patient: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    time = np.linspace(0, 72, 250)
    weight = float(patient["Weight_kg"])
    age = float(patient["Age"])
    bsa = float(patient["BSA"])
    creatinine = float(patient["Serum_Creatinine_mg_dL"])
    bilirubin = float(patient["Bilirubin_mg_dL"])

    clearance = 12.0 * (weight / 70.0) ** 0.75 / (1 + max(creatinine - 1.0, 0) * 0.35)
    clearance *= 1 / (1 + max(bilirubin - 1.0, 0) * 0.25)
    clearance *= 1 / (1 + max(age - 50, 0) * 0.006)
    volume = 40.0 * (bsa / 1.8)
    kel = clearance / volume
    concentration = (100.0 / volume) * np.exp(-kel * time)
    accumulated = concentration + np.roll(concentration, 40) * 0.35
    accumulated[:40] = concentration[:40]
    return time, concentration, accumulated


def render_population_pk(patient: object) -> None:
    st.subheader("Population PK Simulation Module")
    st.caption("Simplified educational visualization only; not intended for clinical decision making.")
    patient_dict = dict(patient)
    time, concentration, accumulated = simulate_population_pk(patient_dict)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=concentration, mode="lines", name="Single-cycle concentration"))
    fig.add_trace(go.Scatter(x=time, y=accumulated, mode="lines", name="Predicted accumulation"))
    fig.update_layout(
        height=450,
        xaxis_title="Time (hours)",
        yaxis_title="Relative concentration",
        title="Concentration-time and accumulation curve",
    )
    st.plotly_chart(fig, use_container_width=True)

    cycle_fig = go.Figure()
    for cycle in range(1, 5):
        cycle_curve = concentration * (1 + 0.12 * (cycle - 1))
        cycle_fig.add_trace(
            go.Scatter(
                x=time + (cycle - 1) * 72,
                y=cycle_curve,
                mode="lines",
                name=f"Cycle {cycle}",
            )
        )
    cycle_fig.update_layout(
        height=450,
        xaxis_title="Time since start (hours)",
        yaxis_title="Relative concentration",
        title="Multi-cycle exposure visualization",
    )
    st.plotly_chart(cycle_fig, use_container_width=True)
