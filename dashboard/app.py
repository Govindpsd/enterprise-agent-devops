import sys
import os
import streamlit as st
import json

# Allow dashboard to import orchestrator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.pipeline import run_incident_pipeline


# ------------------------------------
# Page Config
# ------------------------------------
st.set_page_config(
    page_title="Autonomous AI DevOps Control Center",
    layout="wide"
)

st.title("🚀 Autonomous AI DevOps Control Center")

st.markdown("AI-powered multi-agent autonomous incident response system")

st.divider()

# ------------------------------------
# Incident Input
# ------------------------------------
st.subheader("📝 Enter Incident Description")

user_input = st.text_area(
    "",
    "Checkout service is down. Error rate is 75%. Customers cannot place orders.",
    height=120
)

# ------------------------------------
# Run Pipeline
# ------------------------------------
if st.button("Run Incident Pipeline"):

    st.markdown("## 🚨 Running Autonomous Incident Pipeline...")
    results = run_incident_pipeline(user_input)

    st.divider()

    # ============================================
    # 🔎 INCIDENT CLASSIFICATION
    # ============================================
    st.subheader("🔎 Incident Classification")
    st.json(results.get("incident", {}))

    # ============================================
    # 🧠 ROOT CAUSE DEBATE
    # ============================================
    st.divider()
    st.subheader("🧠 Multi-Agent Root Cause Debate")

    debate = results.get("debate", [])

    if debate:
        cols = st.columns(len(debate))

        for i, hypothesis in enumerate(debate):
            with cols[i]:
                st.markdown(f"### Hypothesis {i+1}")
                st.markdown(f"**Confidence:** {hypothesis.get('confidence', 0)}")
                st.markdown(f"**Root Cause:**")
                st.info(hypothesis.get("root_cause", ""))

                st.markdown("**Evidence:**")
                for ev in hypothesis.get("evidence", []):
                    st.write("-", ev)
    else:
        st.info("No debate hypotheses available.")

    # ============================================
    # ⚙️ ACTION PLAN
    # ============================================
    st.divider()
    st.subheader("⚙️ Action Plan")
    st.json(results.get("actions", {}))

    # ============================================
    # 🛠 REMEDIATION EXECUTION
    # ============================================
    st.divider()
    st.subheader("🛠 Remediation Execution")

    remediation = results.get("remediation", [])

    for step in remediation:
        if step["status"] == "SUCCESS":
            st.success(f"✅ {step['action']}")
        else:
            st.error(f"❌ {step['action']}")

    # ============================================
    # 📊 HEALTH STATUS
    # ============================================
    st.divider()
    st.subheader("📊 System Health")

    health = results.get("health", {})
    error_rate = health.get("error_rate", 0)

    st.progress(min(error_rate / 100, 1.0))

    if error_rate < 30:
        st.success(f"Healthy — Error Rate: {error_rate}%")
    elif error_rate < 70:
        st.warning(f"Degraded — Error Rate: {error_rate}%")
    else:
        st.error(f"Critical — Error Rate: {error_rate}%")

    # ============================================
    # 🧠 DECISION ENGINE
    # ============================================
    st.divider()
    st.subheader("🧠 Decision Engine")

    decision = results.get("decision")

    if decision == "RESOLVED":
        st.success("🎯 Final Decision: RESOLVED")
    elif decision == "RETRY":
        st.warning("🔁 Final Decision: RETRY")
    elif decision == "ESCALATE":
        st.error("🚨 Final Decision: ESCALATE TO JIRA")
    else:
        st.info("No decision returned.")

    # ============================================
    # 🧠 LEARNING MEMORY
    # ============================================
    st.divider()
    st.subheader("🧠 Learning Memory")

    memory = results.get("memory")

    if memory:
        st.write("**Similar Incidents Seen:**", memory.get("similar_count", 0))
        st.write("**Best Historical Action:**", memory.get("best_action", "N/A"))
    else:
        st.info("No historical learning data available yet.")

    # ============================================
    # 🚨 JIRA ESCALATION
    # ============================================
    st.divider()
    st.subheader("🚨 Jira Escalation")

    jira = results.get("jira")

    if jira:
        if jira.get("error"):
            st.error("Jira ticket creation failed.")
            st.json(jira)
        else:
            st.success(f"Issue Created: {jira.get('key')}")
            st.write(jira.get("self"))
    else:
        st.info("No escalation required.")

    st.divider()
    st.success("🏁 Incident Pipeline Completed")
