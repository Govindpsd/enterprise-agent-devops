from orchestrator.agent_client import run_agent


SYSTEM_PROMPT = """
You are an Incident Classification Agent.

You MUST return ONLY valid JSON.
Do not include explanations.

Schema:
{
  "severity": "P1|P2|P3|P4",
  "service": "string",
  "summary": "string",
  "confidence": number
}
"""

def classify_incident(incident_text: str) -> str:
    return run_agent(SYSTEM_PROMPT, incident_text)
