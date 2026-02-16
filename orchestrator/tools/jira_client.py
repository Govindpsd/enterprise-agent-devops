import os
import requests
import json

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
JIRA_ISSUE_TYPE = os.getenv("JIRA_ISSUE_TYPE", "Task")  # Default to "Task" if not set


def create_jira_ticket(jira_payload: dict):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Map P1/P2/P3/P4 → Jira priority
    priority_map = {
        "P1": "Highest",
        "P2": "High",
        "P3": "Medium",
        "P4": "Low"
    }

    jira_priority = priority_map.get(jira_payload.get("priority", "P3"), "Medium")

    # Build comprehensive description
    description_text = jira_payload.get("description", "")
    if jira_payload.get("root_cause"):
        description_text += f"\n\nRoot Cause:\n{jira_payload['root_cause']}"
    if jira_payload.get("recommended_actions"):
        actions = jira_payload["recommended_actions"]
        if isinstance(actions, list):
            actions_text = "\n".join(f"- {action}" for action in actions)
        else:
            actions_text = str(actions)
        description_text += f"\n\nRecommended Actions:\n{actions_text}"

    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": jira_payload["title"],
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description_text
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": JIRA_ISSUE_TYPE
            },
            "priority": {
                "name": jira_priority
            }
        }
    }

    print("Sending Jira Payload:")
    print(json.dumps(payload, indent=2))

    try:
        response = requests.post(
            url,
            headers=headers,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            json=payload
        )

        print("Jira API Status:", response.status_code)
        print("Jira API Response:", response.text)

        if response.status_code == 201:
            return response.json()
        else:
            # Parse error response
            error_data = response.json() if response.text else {}
            error_message = error_data.get("errorMessages", [])
            if error_message:
                error_msg = error_message[0]
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
            
            return {
                "error": True,
                "status_code": response.status_code,
                "message": error_msg,
                "details": error_data
            }
    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "status_code": None,
            "message": f"Request failed: {str(e)}",
            "details": {}
        }
