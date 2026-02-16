import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

AICORE_BASE_URL = os.getenv("AICORE_BASE_URL")
DEPLOYMENT_ID = os.getenv("DEPLOYMENT_ID")
AICORE_CLIENT_ID = os.getenv("AICORE_CLIENT_ID")
AICORE_CLIENT_SECRET = os.getenv("AICORE_CLIENT_SECRET")
AICORE_TOKEN_URL = os.getenv("AICORE_TOKEN_URL")
RESOURCE_GROUP = os.getenv("AICORE_RESOURCE_GROUP", "default")


# -----------------------------
# 1️⃣ Get OAuth Token
# -----------------------------
def get_access_token():
    response = requests.post(
        AICORE_TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(AICORE_CLIENT_ID, AICORE_CLIENT_SECRET),
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get token: {response.text}")

    return response.json()["access_token"]


# -----------------------------
# 2️⃣ Clean JSON (remove ```json blocks)
# -----------------------------
def clean_json_response(content: str) -> str:
    """
    Extracts only JSON from LLM response.
    Removes markdown code fences if present.
    """
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return match.group(0)
    return content.strip()


# -----------------------------
# 3️⃣ Run Agent (LLM Call)
# -----------------------------
def run_agent(system_prompt: str, user_input: str) -> str:
    token = get_access_token()

    url = (
        f"{AICORE_BASE_URL}"
        f"/v2/inference/deployments/{DEPLOYMENT_ID}"
        f"/chat/completions"
        f"?api-version=2024-02-15-preview"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "AI-Resource-Group": RESOURCE_GROUP,
    }

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code != 200:
        raise Exception(f"Model call failed: {response.text}")

    result = response.json()
    content = result["choices"][0]["message"]["content"]
    
    # Clean JSON if wrapped in markdown
    content = clean_json_response(content)
    
    return content
