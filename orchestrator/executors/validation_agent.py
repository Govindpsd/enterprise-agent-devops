import random

def validate_system_health():
    error_rate = random.randint(0, 100)
    return {
        "error_rate": error_rate,
        "status": "STABLE" if error_rate < 20 else "UNSTABLE"
    }
