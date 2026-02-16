from orchestrator.agent_client import run_agent

SYSTEM_PROMPT = """
You are a Jira Ticket Creation Agent.

You receive:
- Incident summary
- Root cause analysis
- Action plan

You MUST return ONLY valid JSON.

Schema:
{
  "title": "string",
  "priority": "P1|P2|P3|P4",
  "description": "string",
  "root_cause": "string",
  "recommended_actions": ["string"]
}
"""

def create_jira_payload(context: str) -> str:
    return run_agent(SYSTEM_PROMPT, context)
