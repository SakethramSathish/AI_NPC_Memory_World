from graphs.state import GraphState
from config import RELATIONSHIP_MIN, RELATIONSHIP_MAX

def clamp(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(value, max_value))

def update_world_state(state: GraphState) -> GraphState:
    """
    Update global world/player reputation based on NPC interaction outcome.
    """

    player = state["player"]
    npc = state["npc"]
    control = state["control"]

    #Use memory importance as signal strength
    importance = control.get("memory_importance", 0.0)

    if importance < 0.3:
        #Interaction too trivial to affect world state
        return state
    
    #Relationship score influences global reputation
    delta = 0
    if npc["mood"] == "hostile":
        delta -= 5
    elif npc["mood"] == "friendly":
        delta += 5

    player["reputation"] += delta
    player["reputation"] = clamp(
        player["reputation"],
        RELATIONSHIP_MIN,
        RELATIONSHIP_MAX,
    )

    return state