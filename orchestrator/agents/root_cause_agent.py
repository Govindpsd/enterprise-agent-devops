from orchestrator.agent_client import run_agent

SYSTEM_PROMPT = """
You are a Root Cause Analysis Agent.

You receive a structured incident summary.
You MUST return ONLY valid JSON.
Do not include explanations.

Schema:
{
  "root_cause": "string",
  "evidence": ["string"],
  "confidence": number
}
"""

def analyze_root_cause(incident_summary: str) -> str:
    return run_agent(SYSTEM_PROMPT, incident_summary)
