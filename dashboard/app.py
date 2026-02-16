# dashboard/app.py

import streamlit as st
import json
from orchestrator.pipeline import run_incident_pipeline

st.set_page_config(page_title="Autonomous DevOps Agent", layout="wide")

st.title("🚀 Autonomous AI DevOps Control Center")

incident_text = st.text_area(
    "Enter Incident Description",
    "Checkout service is down. Error rate is 75%. Customers cannot place orders."
)

if st.button("Run Incident Pipeline"):

    results = run_incident_pipeline(incident_text)

    incident = results["incident"]
    root = results["root_cause"]
    actions = results["actions"]
    remediation = results["remediation"]
    health = results["health"]
    decision = results["decision"]
    jira = results["jira"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔎 Incident Classification")
        st.json(incident)

        st.subheader("🧩 Root Cause")
        st.json(root)

    with col2:
        st.subheader("⚙️ Action Plan")
        st.json(actions)

        st.subheader("🛠 Remediation Results")
        st.json(remediation)

    st.divider()

    st.subheader("📊 Health Status")

    error_rate = health.get("error_rate", 100)
    st.progress(max(0, 100 - error_rate))

    if health["status"] == "STABLE":
        st.success("System Stable ✅")
    else:
        st.warning("System Unstable ⚠️")

    st.divider()

    st.subheader("🧠 Decision Engine")

    if decision == "ESCALATE":
        st.error("Final Decision: ESCALATE 🚨")
    elif decision == "RETRY":
        st.warning("Final Decision: RETRY 🔁")
    else:
        st.success("Final Decision: CLOSE ✅")

    if jira:
        st.subheader("🎫 Jira Escalation")
        st.json(jira)
