from typing import List
from graphs.state import GraphState
from memory.gossip_memory import store_gossip

def spread_gossip(
        state: GraphState,
        all_npc_ids: List[str],
) -> GraphState:
    """
    Spread gossip from the current NPC to other NPCs.
    This is triggered conditionally via LangGraph.
    """

    control = state["control"]
    npc = state["npc"]
    interaction = state["interaction"]

    #If LangGraph says no gossip, exit early
    if not control.get("should_gossip", False):
        return state
    
    source_npc_id = npc["npc_id"]
    npc_name = npc["name"]
    npc_mood = npc["mood"]

    #Gossip Content

    # Load NPC profiles to get personalities
    import json
    from models.llm import get_llm

    try:
        with open("data/npc_profiles.json", "r", encoding="utf-8") as f:
            # Create a dict for easy lookup: { 'npc_eldon': {...}, 'npc_mira': {...} }
            npc_profiles_list = json.load(f)
            npc_profiles = {n["npc_id"]: n for n in npc_profiles_list}
            
    except Exception:
        npc_profiles = {}

    llm = get_llm()

    #Confidence is derived from memory importance
    confidence = min(1.0, control.get("memory_importance", 0.8))

    #Spread to other NPCs

    for target_npc_id in all_npc_ids:
        if target_npc_id == source_npc_id:
            continue
        
        target_npc_data = npc_profiles.get(target_npc_id, {"name": target_npc_id, "personality": "Unknown"})
        
        # Generate dynamic gossip conversation
        prompt = f"""
You are simulating a short conversation between two NPCs in a game world.
The topic is the PLAYER, who just interacted with {npc_name}.

SOURCE NPC: {npc_name} (Personality: {npc['personality']}, Mood: {npc_mood})
TARGET NPC: {target_npc_data['name']} (Personality: {target_npc_data['personality']})

CONTEXT:
The player said: "{interaction['player_input']}"
{npc_name} responded: "{interaction['npc_response']}"
{npc_name}'s current feeling is: {npc_mood}

TASK:
Write a SHORT dialogue (2-3 lines max) where {npc_name} tells {target_npc_data['name']} about this interaction, and {target_npc_data['name']} responds in character.
Format it like a script.

Example:
{npc_name}: "Can you believe what the player just said?"
{target_npc_data['name']}: "Typical behavior from them. I'm not surprised."
""".strip()

        try:
             gossip_content = llm.generate(prompt=prompt)
        except Exception:
             # Fallback
             gossip_content = f"{npc_name} told {target_npc_data['name']} about the player's recent behavior."

        store_gossip(
            target_npc_id=target_npc_id,
            source_npc_id=source_npc_id,
            content=gossip_content,
            emotion=npc_mood,
            confidence=confidence,
        )
        print(f"DEBUG: Gossip spread from {source_npc_id} to {target_npc_id}")

    return state