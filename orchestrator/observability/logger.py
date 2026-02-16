import datetime
import json

def log_event(stage: str, payload):
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    print("\n" + "━" * 50)
    print(f"[{timestamp}] STAGE: {stage}")
    print("━" * 50)

    try:
        # Pretty print JSON if possible
        parsed = json.loads(payload)
        print(json.dumps(parsed, indent=2))
    except Exception:
        # Fallback for non-JSON payloads
        print(payload)

    print("━" * 50 + "\n")
