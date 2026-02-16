# orchestrator/agents/consensus_agent.py

import json

def choose_best_hypothesis(hypotheses):
    """
    Selects hypothesis with highest confidence.
    You can later upgrade this to weighted scoring.
    """

    best = max(hypotheses, key=lambda x: x["confidence"])

    return {
        "selected_agent": best["agent"],
        "root_cause": best["hypothesis"],
        "confidence": best["confidence"],
        "reasoning": best["reasoning"]
    }
