from ai_core_client import call_chat_completion

DEPLOYMENT_ID = "d06b1ca54a850d65"

messages = [
    {"role": "system", "content": "You are a test agent. Respond in JSON only."},
    {"role": "user", "content": "Say hello in JSON format."}
]

response = call_chat_completion(DEPLOYMENT_ID, messages)

print(response)
