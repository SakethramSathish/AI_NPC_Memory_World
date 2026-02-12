from typing import Dict
from config import RELATIONSHIP_MIN, RELATIONSHIP_MAX

def clamp(value: int) -> int:
    """
    Clamp relationship score within bounds.
    """
    return max(RELATIONSHIP_MIN, min(RELATIONSHIP_MAX, value))


def calculate_relationship_delta(
        sentiment: str,
        intensity: int,
) -> int:
    """
    Convert sentiment into relationship change.
    """

    if sentiment == "positive":
        delta = 5 + intensity * 2
    elif sentiment == "negative":
        delta = -5 - intensity * 2
    else:
        delta = 0

    return delta

def get_relationship_status(score: int) -> str:
    """
    Get the text description of the relationship based on score.
    """
    if score <= -50:
        return "Hostile"
    elif score <= -10:
        return "Cold"
    elif score <= 10:
        return "Neutral"
    elif score <= 50:
        return "Friendly"
    else:
        return "Loyal"