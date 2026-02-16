from orchestrator.agent_client import run_agent

SYSTEM_PROMPT = """
You are an Action Planning Agent for DevOps incidents.

You receive a structured root cause analysis.
You MUST return ONLY valid JSON.
Do not include explanations.

Schema:
{
  "actions": ["string"],
  "priority": "Immediate|High|Medium|Low",
  "confidence": number
}
"""

def plan_actions(root_cause_summary: str) -> str:
    return run_agent(SYSTEM_PROMPT, root_cause_summary)
