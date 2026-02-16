# orchestrator/agents/hypothesis_agents.py

from orchestrator.agent_client import run_agent
import json

DB_PROMPT = """
You are a senior database reliability engineer.
Analyze the incident and propose a database-related root cause hypothesis.

Respond strictly in JSON:
{
  "agent": "DB",
  "hypothesis": "...",
  "confidence": 0-1,
  "reasoning": "..."
}
"""

INFRA_PROMPT = """
You are a cloud infrastructure SRE.
Analyze the incident and propose an infrastructure-related root cause hypothesis.

Respond strictly in JSON:
{
  "agent": "INFRA",
  "hypothesis": "...",
  "confidence": 0-1,
  "reasoning": "..."
}
"""

APP_PROMPT = """
You are an application performance engineer.
Analyze the incident and propose an application-layer root cause hypothesis.

Respond strictly in JSON:
{
  "agent": "APP",
  "hypothesis": "...",
  "confidence": 0-1,
  "reasoning": "..."
}
"""


def generate_hypotheses(incident_text: str):
    db = json.loads(run_agent(DB_PROMPT, incident_text))
    infra = json.loads(run_agent(INFRA_PROMPT, incident_text))
    app = json.loads(run_agent(APP_PROMPT, incident_text))

    return [db, infra, app]
