def evaluate_decision(
    incident_result: dict,
    root_cause_result: dict,
    action_result: dict,
    remediation_results: list,
    health_status: dict,
    attempt: int,
    max_attempts: int = 2
):
    severity = incident_result.get("severity")
    incident_conf = incident_result.get("confidence", 0)
    root_conf = root_cause_result.get("confidence", 0)
    action_conf = action_result.get("confidence", 0)

    total_actions = len(remediation_results)
    successful_actions = sum(
        1 for r in remediation_results if r["status"] == "SUCCESS"
    )

    success_rate = successful_actions / total_actions if total_actions else 0
    error_rate = health_status.get("error_rate", 100)

    print("\n🧠 Decision Engine Analysis")
    print("Severity:", severity)
    print("Confidence:", incident_conf, root_conf, action_conf)
    print("Remediation Success Rate:", success_rate)
    print("Error Rate:", error_rate)
    print("Attempt:", attempt)

    if error_rate < 10:
        return "CLOSE"

    if success_rate >= 0.75 and attempt < max_attempts:
        return "RETRY"

    if severity == "P1" and error_rate > 20:
        return "ESCALATE"

    if min(incident_conf, root_conf, action_conf) < 0.7:
        return "ESCALATE"

    return "ESCALATE"
