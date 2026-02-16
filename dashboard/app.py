import streamlit as st
import time
from orchestrator.main import run_incident_pipeline

st.set_page_config(page_title="Autonomous AI Control Room", layout="wide")

st.title("🧠 Autonomous AI Operations Control Room")
st.markdown("Live Multi-Agent Enterprise System")

incident_input = st.text_area(
    "Enter Incident Description",
    "Checkout service is down. Error rate is 75%. Customers cannot place orders."
)

if st.button("🚨 Trigger Autonomous Response"):

    with st.spinner("AI is diagnosing the system..."):
        results = run_incident_pipeline(incident_input)

    st.subheader("🔎 Incident Classification")
    st.json(results["incident"])

    st.subheader("🧩 Root Cause Analysis")
    st.json(results["root_cause"])

    st.subheader("⚙️ Action Plan")
    st.json(results["actions"])

    st.subheader("🛠 Remediation Execution")
    st.json(results["remediation"])

    st.subheader("📊 System Health")
    st.json(results["health"])

    if results["health"]["status"] == "STABLE":
        st.success("✅ Incident Resolved Autonomously")
    else:
        st.error("⚠️ Escalated to Jira")
        st.json(results["jira"])
