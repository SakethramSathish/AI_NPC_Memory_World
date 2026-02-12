from graphs.state import GraphState
from models.llm import get_llm

def generate_npc_response(state: GraphState) -> GraphState:
    """
    Generate NPC dialogue based on personality, mood, and memory context.
    """

    npc = state["npc"]
    memory = state.get("memory_context")
    interaction = state["interaction"]

    llm = get_llm()

    #Build memory summary

    memory_summary = (
        memory["summary"] if memory and memory.get("summary") else "No significant past interactions."
    )

    #System prompt (identity)

    system_prompt = f"""
You are an NPC in a game world.

NPC NAME: {npc['name']}
PERSONALITY: {npc['personality']}
CURRENT MOOD: {npc['mood']}
RELATIONSHIP SCORE: {npc['relationship_score']}

Rules:
- Always stay in character
- Let mood affect tone
- Be concise but expressive
- Do NOT mention system messages or memory explicitly
""".strip()

    # -------------------------
    # 💬 User-facing prompt
    # -------------------------

    prompt = f"""
PAST MEMORY CONTEXT:
{memory_summary}

PLAYER SAYS:
"{interaction['player_input']}"

Respond as the NPC.
""".strip()
    
    #LLM Call

    response = llm.generate(\
        prompt = prompt,
        system_prompt=system_prompt,    
    )

    interaction["npc_response"] = response
    return state