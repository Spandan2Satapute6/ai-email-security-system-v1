from typing import Dict, Any


def grade(observation: Dict[str, Any], task: str) -> float:
    """
    Meta OpenEnv Grader (FINAL FIXED)

    Always returns score strictly in (0,1)
    """

    try:
        intent = str(observation.get("intent", "safe")).lower()
        confidence = float(observation.get("confidence", 0.5))
        risk = str(observation.get("risk_level", "low")).lower()
        explanation = str(observation.get("explanation", "")).lower()

        # Normalize confidence
        confidence = max(0.0, min(1.0, confidence))

        # Route to task grader
        if task == "easy_task":
            score = grade_easy(intent)

        elif task == "medium_task":
            score = grade_medium(intent, confidence)

        elif task == "hard_task":
            score = grade_hard(intent, confidence, risk, explanation)

        else:
            score = 0.5

    except Exception:
        score = 0.5

    # 🔥 CRITICAL: FORCE INTO (0,1)
    score = max(0.1, min(0.9, score))

    return float(score)


# ---------------- EASY ----------------
def grade_easy(intent: str) -> float:
    valid = ["spam", "safe", "phishing", "suspicious"]

    if intent in valid:
        return 0.7
    else:
        return 0.3


# ---------------- MEDIUM ----------------
def grade_medium(intent: str, confidence: float) -> float:
    valid = ["spam", "safe", "phishing", "suspicious"]

    score = 0.0

    # intent (0.4)
    if intent in valid:
        score += 0.4

    # confidence (0.4)
    if confidence > 0.6:
        score += 0.4
    else:
        score += 0.2

    return score


# ---------------- HARD ----------------
def grade_hard(intent: str, confidence: float, risk: str, explanation: str) -> float:
    valid = ["spam", "safe", "phishing", "suspicious"]

    score = 0.0

    # intent (0.3)
    if intent in valid:
        score += 0.3

    # confidence (0.3)
    if confidence > 0.6:
        score += 0.3
    else:
        score += 0.15

    # risk (0.2)
    expected_risk = "high" if intent in ["spam", "phishing"] else "low"
    if risk == expected_risk:
        score += 0.2
    else:
        score += 0.1

    # explanation (0.2)
    if len(explanation) > 10:
        score += 0.2
    else:
        score += 0.1

    return score