from graphs.state import GraphState
from config import RELATIONSHIP_MIN, RELATIONSHIP_MAX

def clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))

def update_emotion(state: GraphState) -> GraphState:
    """
    Update NPC mood and relationship score based on retrieved memory.
    This function is deterministic and does not use an LLM
    """

    npc = state["npc"]
    memory = state.get("memory_context")

    #If no memory retrieved, keep NPC neutral
    if not memory:
        npc["mood"] = "neutral"
        return state
    
    dominant_emotion = memory.get("dominant_emotion")
    trust_delta = memory.get("trust_delta_estimate", 0)

    #Mood Determination

    if dominant_emotion in ("anger", "distrust"):
        npc["mood"] = "hostile"
    elif dominant_emotion in ("trust", "gratitude"):
        npc["mood"] = "friendly"
    else:
        npc["mood"] = "neutral"

    #Relationship Update

    npc["relationship_score"] += trust_delta
    npc["relationship_score"] = clamp(
        npc["relationship_score"],
        RELATIONSHIP_MIN,
        RELATIONSHIP_MAX
    )

    return state