import requests
from orchestrator.config import CLIENT_ID, CLIENT_SECRET, TOKEN_URL, AI_CORE_BASE_URL


def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    response.raise_for_status()
    return response.json()["access_token"]


def call_chat_completion(deployment_id, messages):
    token = get_access_token()

    url = (
        f"{AI_CORE_BASE_URL}"
        f"/v2/inference/deployments/{deployment_id}"
        f"/chat/completions"
        f"?api-version=2024-02-15-preview"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "AI-Resource-Group": "default"
    }

    payload = {
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 300
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    response.raise_for_status()
    return response.json()
