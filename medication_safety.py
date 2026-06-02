from __future__ import annotations

import pandas as pd
import streamlit as st


INTERACTION_RULES = {
    frozenset({"ondansetron", "dexamethasone"}): (
        "Low",
        "Common supportive care combination; educational review point for steroid and antiemetic overlap.",
    ),
    frozenset({"cisplatin", "furosemide"}): (
        "Moderate",
        "Educational alert: nephrotoxic or ototoxic exposure context may require careful review.",
    ),
    frozenset({"methotrexate", "NSAID"}): (
        "High",
        "Educational alert for a known interaction pattern with potential renal clearance impact.",
    ),
}

HIGH_RISK_DRUGS = {
    "cisplatin": "High-risk platinum agent with renal, auditory, and electrolyte monitoring considerations.",
    "doxorubicin": "Anthracycline with cumulative exposure and cardiotoxicity education relevance.",
    "methotrexate": "High-alert antimetabolite requiring strong medication safety awareness.",
    "vincristine": "Neurotoxic vinca alkaloid; route and administration safety are critical.",
}


def _normalize_drug_name(drug_name: str) -> str:
    return str(drug_name).strip().lower()


def _split_medications(values: pd.Series) -> set[str]:
    meds: set[str] = set()
    for raw_value in values.dropna().astype(str):
        for token in raw_value.split(";"):
            normalized = _normalize_drug_name(token)
            if normalized:
                meds.add(normalized)
    return meds


def review_interactions(treatment_df: pd.DataFrame) -> pd.DataFrame:
    drugs = {_normalize_drug_name(x) for x in treatment_df["Drug_Administered"].unique()}
    supportive = _split_medications(treatment_df["Supportive_Care_Medications"])
    observations = []
    for pair, (severity, rationale) in INTERACTION_RULES.items():
        if pair.issubset(drugs | supportive):
            observations.append(
                {
                    "Finding": "Potential interaction pattern",
                    "Severity": severity,
                    "Clinical_Rationale": rationale,
                }
            )
    return pd.DataFrame(observations)


def detect_duplicate_therapy(treatment_df: pd.DataFrame) -> pd.DataFrame:
    duplicates = (
        treatment_df.groupby(["Treatment_Date", "Cycle_Number", "Drug_Administered"])
        .size()
        .reset_index(name="Occurrences")
    )
    duplicates = duplicates[duplicates["Occurrences"] > 1].copy()
    if duplicates.empty:
        return pd.DataFrame(columns=["Finding", "Severity", "Clinical_Rationale"])
    duplicates["Severity"] = "Moderate"
    duplicates["Clinical_Rationale"] = (
        "Potential repeated administration within the same cycle/date was identified for educational review."
    )
    duplicates.rename(columns={"Drug_Administered": "Finding"}, inplace=True)
    return duplicates[["Finding", "Severity", "Clinical_Rationale"]]


def organ_function_review(patient: pd.Series) -> pd.DataFrame:
    observations = [
        {
            "Finding": "Renal function",
            "Severity": "Info" if float(patient["Serum_Creatinine_mg_dL"]) < 1.5 else "Moderate",
            "Clinical_Rationale": "Educational renal function context based on serum creatinine.",
        },
        {
            "Finding": "Hepatic function",
            "Severity": "Info" if float(patient["Bilirubin_mg_dL"]) < 1.2 else "Moderate",
            "Clinical_Rationale": "Educational hepatic function context based on bilirubin and transaminases.",
        },
    ]
    return pd.DataFrame(observations)


def high_risk_medications(treatment_df: pd.DataFrame) -> pd.DataFrame:
    matches = []
    for drug in treatment_df["Drug_Administered"].unique():
        if _normalize_drug_name(drug) in HIGH_RISK_DRUGS:
            matches.append(
                {
                    "Finding": drug,
                    "Severity": "High",
                    "Clinical_Rationale": HIGH_RISK_DRUGS[_normalize_drug_name(drug)],
                }
            )
    return pd.DataFrame(matches)


def render_medication_safety(patient: pd.Series, treatment_df: pd.DataFrame) -> None:
    st.subheader("Medication Safety Module")
    st.caption("Educational workflow support for oncology pharmacy medication review.")

    sections = {
        "Drug-Drug Interaction Review": review_interactions(treatment_df),
        "Duplicate Therapy Detection": detect_duplicate_therapy(treatment_df),
        "Organ Function Safety Review": organ_function_review(patient),
        "High-Risk Medication Identification": high_risk_medications(treatment_df),
    }

    for title, frame in sections.items():
        st.markdown(f"#### {title}")
        if frame.empty:
            st.success("No educational flags identified in the current sample data.")
        else:
            st.dataframe(frame, use_container_width=True, hide_index=True)
