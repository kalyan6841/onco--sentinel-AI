import streamlit as st

from patient_profile import load_patient_profiles, render_patient_summary
from treatment_journey import load_treatment_journey, render_treatment_journey
from exposure_engine import render_exposure_engine
from medication_safety import render_medication_safety
from toxicity_engine import render_toxicity_engine
from pkpd_engine import render_pkpd_engine
from population_pk import render_population_pk
from precision_oncology import render_precision_oncology
from research_dashboard import render_research_dashboard


st.set_page_config(
    page_title="Onco-Sentinel AI",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

SAFETY_STATEMENT = (
    "Onco-Sentinel AI is an educational and research-oriented prototype. "
    "It does not provide medical advice, treatment recommendations, or replace clinician judgement. "
    "All treatment decisions remain the responsibility of qualified healthcare professionals."
)


def render_header() -> None:
    st.title("Onco-Sentinel AI")
    st.caption(
        "Oncology clinical intelligence for educational visualization, exposure tracking, and workflow support."
    )
    st.info(SAFETY_STATEMENT)


def main() -> None:
    render_header()
    profiles = load_patient_profiles()
    treatment = load_treatment_journey()

    st.sidebar.header("Patient Selection")
    patient_id = st.sidebar.selectbox("Select Patient ID", profiles["Patient_ID"].tolist())
    patient = profiles.loc[profiles["Patient_ID"] == patient_id].iloc[0]
    patient_treatment = treatment[treatment["Patient_ID"] == patient_id].copy()

    tab_labels = [
        "Patient Profile",
        "Treatment Journey",
        "Exposure Engine",
        "Medication Safety",
        "Toxicity Intelligence",
        "PK/PD Intelligence",
        "Population PK",
        "Precision Oncology",
        "Research Dashboard",
    ]

    tabs = st.tabs(tab_labels)

    with tabs[0]:
        render_patient_summary(patient)
    with tabs[1]:
        render_treatment_journey(patient_treatment, patient_id=patient_id)
    with tabs[2]:
        render_exposure_engine(patient_treatment)
    with tabs[3]:
        render_medication_safety(patient, patient_treatment)
    with tabs[4]:
        render_toxicity_engine(patient, patient_treatment)
    with tabs[5]:
        render_pkpd_engine()
    with tabs[6]:
        render_population_pk(patient)
    with tabs[7]:
        render_precision_oncology()
    with tabs[8]:
        render_research_dashboard(patient, patient_treatment)


if __name__ == "__main__":
    main()
