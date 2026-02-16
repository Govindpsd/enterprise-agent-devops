# orchestrator/main.py

from orchestrator.pipeline import run_incident_pipeline
import json

if __name__ == "__main__":

    incident_text = """
    Checkout service is down.
    Error rate is 75%.
    Customers cannot place orders.
    """

    results = run_incident_pipeline(incident_text)

    print("\n🔎 Incident Classification")
    print(json.dumps(results["incident"], indent=2))

    print("\n🧩 Root Cause")
    print(json.dumps(results["root_cause"], indent=2))

    print("\n⚙️ Action Plan")
    print(json.dumps(results["actions"], indent=2))

    print("\n🛠 Remediation Execution")
    print(json.dumps(results["remediation"], indent=2))

    print("\n📊 Health Status")
    print(json.dumps(results["health"], indent=2))

    if results["health"]["status"] == "STABLE":
        print("\n✅ Incident Resolved Autonomously")
    else:
        print("\n⚠️ Escalated to Jira")
        print(json.dumps(results["jira"], indent=2))
