import random

def execute_actions(actions):
    results = []
    for action in actions:
        success = random.random() > 0.2
        results.append({
            "action": action,
            "status": "SUCCESS" if success else "FAILED"
        })
    return results
