from __future__ import annotations

import streamlit as st


BIOMARKERS = {
    "EGFR": "Educational placeholder for receptor tyrosine kinase pathway relevance.",
    "KRAS": "Educational placeholder for MAPK pathway signaling biology.",
    "BRAF": "Educational placeholder for downstream pathway activation and mutation context.",
    "ALK": "Educational placeholder for fusion-driven oncogenic signaling biology.",
    "HER2": "Educational placeholder for receptor overexpression and targeted therapy research context.",
    "TP53": "Educational placeholder for tumor suppressor pathway and genomic instability context.",
}


def render_precision_oncology() -> None:
    st.subheader("Precision Oncology Readiness Layer")
    st.caption("Future integration placeholders for biomarker-aware research workflows.")
    for biomarker, note in BIOMARKERS.items():
        with st.expander(biomarker):
            st.write(note)
            st.info("No treatment recommendations are provided.")
