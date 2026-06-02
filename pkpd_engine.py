from __future__ import annotations

import streamlit as st


PKPD_LIBRARY = {
    "Doxorubicin": {
        "Mechanism": "Anthracycline that intercalates DNA and inhibits topoisomerase II.",
        "PK": "Extensive tissue distribution, hepatic metabolism, and biliary elimination.",
        "PD": "Concentration and cumulative exposure relate to antitumor activity and toxicity education.",
        "Half_Life": "~20-48 h",
        "Vd": "Large",
        "Clearance": "Hepatic",
        "Metabolism": "Hepatic carbonyl reduction",
        "Organ_Considerations": "Cardiac and hepatic monitoring considerations are commonly discussed in education.",
    },
    "Paclitaxel": {
        "Mechanism": "Microtubule-stabilizing taxane that inhibits mitosis.",
        "PK": "Nonlinear disposition in some settings; hepatic elimination is a key educational theme.",
        "PD": "Exposure-related neuropathy and myelosuppression are common teaching points.",
        "Half_Life": "Variable",
        "Vd": "Large",
        "Clearance": "Hepatic",
        "Metabolism": "CYP2C8 / CYP3A4",
        "Organ_Considerations": "Liver function and peripheral neuropathy monitoring are relevant educational considerations.",
    },
    "Cyclophosphamide": {
        "Mechanism": "Alkylating agent requiring bioactivation.",
        "PK": "Prodrug activation occurs mainly in the liver.",
        "PD": "Dose exposure relates to myelosuppression and urothelial toxicity education.",
        "Half_Life": "~3-12 h",
        "Vd": "Moderate",
        "Clearance": "Renal and hepatic",
        "Metabolism": "Hepatic activation via CYP enzymes",
        "Organ_Considerations": "Renal and hepatic function are common educational review points.",
    },
}


def render_pkpd_engine() -> None:
    st.subheader("PK/PD Intelligence Module")
    drug = st.selectbox("Select oncology drug", list(PKPD_LIBRARY.keys()))
    info = PKPD_LIBRARY[drug]

    for label, value in info.items():
        st.markdown(f"**{label.replace('_', ' ')}:** {value}")

    st.info("Educational information only. No dosing, treatment, or therapy optimization guidance is provided.")
