# dashboard/app.py

import os
import sys
import json
import streamlit as st

# Fix import path so orchestrator module works
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.pipeline import run_incident_pipeline


# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Autonomous AI DevOps Control Center",
    layout="wide"
)

st.title("🚀 Autonomous AI DevOps Control Center")

st.markdown("---")


# ---------------------------
# Incident Input
# ---------------------------
incident_text = st.text_area(
    "Enter Incident Description",
    value="Checkout service is down. Error rate is 75%. Customers cannot place orders.",
    height=120,
    key="incident_input"
)

run_button = st.button(
    "Run Incident Pipeline",
    key="run_pipeline_button"
)


# ---------------------------
# Run Pipeline
# ---------------------------
if run_button:

    with st.spinner("Running Autonomous Incident Pipeline..."):
        results = run_incident_pipeline(incident_text)

    st.success("Incident Pipeline Completed")

    st.markdown("---")

    # ==========================================
    # 📊 SYSTEM HEALTH
    # ==========================================
    st.subheader("📊 System Health")

    health = results.get("health", {})
    error_rate = health.get("error_rate", 0)
    status = health.get("status", "UNKNOWN")

    st.progress(min(error_rate / 100, 1.0))

    if status == "STABLE":
        st.success(f"Stable — Error Rate: {error_rate}%")
    elif status == "DEGRADED":
        st.warning(f"Degraded — Error Rate: {error_rate}%")
    else:
        st.error(f"Unstable — Error Rate: {error_rate}%")

    st.markdown("---")

    # ==========================================
    # 🧠 DECISION ENGINE
    # ==========================================
    st.subheader("🧠 Decision Engine")

    decision = results.get("decision", "UNKNOWN")

    if decision == "RESOLVED":
        st.success("✅ Final Decision: RESOLVED")
    elif decision == "RETRY":
        st.warning("🔁 Final Decision: RETRY")
    elif decision == "ESCALATE":
        st.error("🚨 Final Decision: ESCALATE TO JIRA")
    else:
        st.info(f"Decision: {decision}")

    st.markdown("---")

    # ==========================================
    # 🧩 MULTI-AGENT DEBATE
    # ==========================================
    st.subheader("🧩 Multi-Agent Root Cause Debate")

    debate = results.get("debate", [])

    if debate:
        for i, hypothesis in enumerate(debate):
            with st.expander(f"Hypothesis {i+1}: {hypothesis.get('root_cause', 'Unknown')}"):
                st.write("Confidence:", hypothesis.get("confidence", "N/A"))
                st.write("Evidence:")
                for ev in hypothesis.get("evidence", []):
                    st.write("•", ev)
    else:
        st.info("No debate data available.")

    st.markdown("---")

    # ==========================================
    # 🧠 LEARNING MEMORY
    # ==========================================
    st.subheader("🧠 Learning Memory")

    memory = results.get("memory", [])

    if memory:
        for entry in memory[-5:]:
            with st.expander(f"{entry.get('service')} — {entry.get('decision')}"):
                st.json(entry)
    else:
        st.info("No historical learning data available yet.")

    st.markdown("---")

    # ==========================================
    # 🎫 JIRA ESCALATION
    # ==========================================
    st.subheader("🎫 Jira Escalation")

    jira = results.get("jira")

    if jira:
        if jira.get("key"):
            st.success(f"Issue Created: {jira['key']}")
            st.write(jira.get("self"))
        elif jira.get("error"):
            st.error("Jira Escalation Failed")
            st.write(jira.get("message"))
        else:
            st.info("No Jira escalation needed.")
    else:
        st.info("No Jira action taken.")
