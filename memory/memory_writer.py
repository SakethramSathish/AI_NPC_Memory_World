from typing import Dict
from datetime import datetime, timezone
from memory.chroma_client import ChromaClient
from graphs.state import GraphState
from config import (
    MEMORY_IMPORTANCE_THRESHOLD,
    GOSSIP_IMPORTANCE_THRESHOLD,
)

def store_memory(state: GraphState) -> GraphState:
    """
    Store the current interaction as memory if required.
    Updates control flags for gossip and persistance.
    """

    npc = state["npc"]
    interaction = state["interaction"]
    control = state["control"]

    npc_id = npc["npc_id"]
    player_input = interaction["player_input"]
    npc_response = interaction.get("npc_response", "")

    #Determine Memory Impact

    importance = control.get("memory_importance", 0.0)

    if importance < MEMORY_IMPORTANCE_THRESHOLD:
        control["should_store_memory"] = False
        control["should_gossip"] = False
        return state
    
    #Prepare memory object

    memory_text = f"Player said: '{player_input}'. NPC replied: '{npc_response}'"

    metadata: Dict = {
        "npc_id": npc_id,
        "emotion": npc["mood"],
        "impact_score": npc["relationship_score"],
        "source": "direct",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    #Store in Chroma

    collection = ChromaClient.get_collection(f"npc_memories_{npc_id}")

    collection.add(
        documents = [memory_text],
        metadatas = [metadata],
        ids = [f"{npc_id}_{metadata['timestamp']}"],
    )

    #Update control flags

    control["should_store_memory"] = True
    control["should_gossip"] = importance >= GOSSIP_IMPORTANCE_THRESHOLD

    return state