# # orchestrator/pipeline.py

# import json
# from orchestrator.agents.incident_agent import classify_incident
# from orchestrator.agents.root_cause_agent import analyze_root_cause
# from orchestrator.agents.action_agent import plan_actions
# from orchestrator.executors.remediation_engine import execute_actions
# from orchestrator.executors.validation_agent import validate_system_health
# from orchestrator.tools.jira_client import create_jira_ticket
# from orchestrator.decision_engine import evaluate_decision




# def run_incident_pipeline(incident_text: str) -> dict:
#     """
#     Runs the full autonomous incident lifecycle:
#     1. Classification
#     2. Root cause analysis
#     3. Action planning
#     4. Remediation execution
#     5. Health validation
#     6. Jira escalation (if needed)
#     """

#     # Step 1 — Incident classification
#     incident_result = json.loads(classify_incident(incident_text))

#     # Step 2 — Root cause
#     root_cause_result = json.loads(analyze_root_cause(json.dumps(incident_result)))

#     # Step 3 — Action planning
#     action_result = json.loads(plan_actions(json.dumps(root_cause_result)))

#     # Step 4 — Execute remediation
#     remediation_result = execute_actions(action_result["actions"])

#     # Step 5 — Validate system health
#     health_status = validate_system_health()

#     # Step 6 — Escalate to Jira only if unstable
#     jira_result = None
#     if health_status["status"] != "STABLE":
#         from orchestrator.agents.jira_agent import create_jira_payload
        
#         # Combine context for Jira agent
#         context = json.dumps({
#             "incident": incident_result,
#             "root_cause": root_cause_result,
#             "action_plan": action_result
#         })
        
#         # Get Jira ticket payload from agent
#         jira_payload_str = create_jira_payload(context)
#         jira_payload = json.loads(jira_payload_str)
        
#         # Map priority from P1/P2/P3/P4 to Jira format if needed
#         priority_map = {"P1": "Highest", "P2": "High", "P3": "Medium", "P4": "Low"}
#         if "priority" in jira_payload and jira_payload["priority"] in priority_map:
#             jira_payload["priority"] = priority_map[jira_payload["priority"]]
        
#         # Create the Jira ticket (handle errors gracefully)
#         try:
#             jira_result = create_jira_ticket(jira_payload)
#             if jira_result.get("error"):
#                 print(f"⚠️  Jira ticket creation failed: {jira_result.get('message')}")
#         except Exception as e:
#             print(f"⚠️  Jira ticket creation failed with exception: {str(e)}")
#             jira_result = {
#                 "error": True,
#                 "message": str(e)
#             }

#     return {
#         "incident": incident_result,
#         "root_cause": root_cause_result,
#         "actions": action_result,
#         "remediation": remediation_result,
#         "health": health_status,
#         "jira": jira_result
#     }

# orchestrator/pipeline.py

import json

from orchestrator.agents.incident_agent import classify_incident
from orchestrator.agents.root_cause_agent import analyze_root_cause
from orchestrator.agents.action_agent import plan_actions
from orchestrator.executors.remediation_engine import execute_actions
from orchestrator.executors.validation_agent import validate_system_health
from orchestrator.tools.jira_client import create_jira_ticket
from orchestrator.decision_engine import evaluate_decision
from orchestrator.memory.store import save_memory, find_similar_incident
from orchestrator.agents.hypothesis_agents import generate_hypotheses
from orchestrator.agents.consensus_agent import choose_best_hypothesis




def run_incident_pipeline(incident_text: str) -> dict:
    """
    Runs the full autonomous incident lifecycle:
    1. Classification
    2. Root cause analysis
    3. Action planning
    4. Remediation execution
    5. Health validation
    6. Intelligent decision engine (Retry / Escalate / Close)
    """

    print("\n🚨 Starting Incident Pipeline\n")

    # ---------------------------------------------------
    # Step 1 — Incident classification
    # ---------------------------------------------------
    incident_result = json.loads(classify_incident(incident_text))
    print("\n🔎 Incident Classification")
    print(json.dumps(incident_result, indent=2))

    similar = find_similar_incident(incident_result["service"])
    if similar:
        print("🧠 Found similar historical incident. Reusing previous solution.")

    # ---------------------------------------------------
    # Step 2 — Root cause
    # ---------------------------------------------------
    
    # Step 2 — Multi-agent debate

    hypotheses = generate_hypotheses(json.dumps(incident_result))

    print("\n🧠 Hypothesis Debate Results:")
    for h in hypotheses:
        print(h)

    root_cause_result = choose_best_hypothesis(hypotheses)

    print("\n🧩 Root Cause")
    print(json.dumps(root_cause_result, indent=2))

    # ---------------------------------------------------
    # Step 3 — Action planning
    # ---------------------------------------------------
    action_result = json.loads(
        plan_actions(json.dumps(root_cause_result))
    )
    print("\n⚙️ Action Plan")
    print(json.dumps(action_result, indent=2))

    # ---------------------------------------------------
    # Step 4 — Execute remediation
    # ---------------------------------------------------
    remediation_result = execute_actions(action_result["actions"])
    print("\n🛠 Remediation Execution")
    print(json.dumps(remediation_result, indent=2))

    # ---------------------------------------------------
    # Step 5 — Validate system health
    # ---------------------------------------------------
    health_status = validate_system_health()
    print("\n📊 Health Status")
    print(json.dumps(health_status, indent=2))

    # ---------------------------------------------------
    # Step 6 — Intelligent Decision Engine
    # ---------------------------------------------------
    jira_result = None

    decision = evaluate_decision(
        incident_result=incident_result,
        root_cause_result=root_cause_result,
        action_result=action_result,
        remediation_results=remediation_result,
        health_status=health_status,
        attempt=1,  # Can be dynamic later
    )

    print("\n🎯 Final Decision:", decision)

    # ---------------------------------------------------
    # Decision Handling
    # ---------------------------------------------------

    if decision == "ESCALATE":
        print("\n⚠️ Escalating to Jira...")

        from orchestrator.agents.jira_agent import create_jira_payload

        context = json.dumps({
            "incident": incident_result,
            "root_cause": root_cause_result,
            "action_plan": action_result
        })

        jira_payload_str = create_jira_payload(context)
        jira_payload = json.loads(jira_payload_str)

        # Map priority P1-P4 → Jira priorities
        priority_map = {
            "P1": "Highest",
            "P2": "High",
            "P3": "Medium",
            "P4": "Low"
        }

        if "priority" in jira_payload and jira_payload["priority"] in priority_map:
            jira_payload["priority"] = priority_map[jira_payload["priority"]]

        try:
            jira_result = create_jira_ticket(jira_payload)
            if jira_result:
                print("\n⚠️ Escalated to Jira")
                print(json.dumps(jira_result, indent=2))
            else:
                print("\n⚠️ Jira ticket creation failed")
        except Exception as e:
            print("\n⚠️ Jira ticket creation failed")

    elif decision == "RETRY":
        print("\n🔁 Retrying remediation logic (simulation)...")

    elif decision == "CLOSE":
        print("\n✅ Incident resolved. No escalation required.")

    save_memory({
    "service": incident_result["service"],
    "root_cause": root_cause_result["root_cause"],
    "successful_actions": [
        r["action"] for r in remediation_result if r["status"] == "SUCCESS"
    ]
})


    return {
    "incident": incident_result,
    "hypotheses": hypotheses,   # ← add this
    "root_cause": root_cause_result,
    "actions": action_result,
    "remediation": remediation_result,
    "health": health_status,
    "decision": decision,
    "jira": jira_result
}


