from typing import Dict
from models.llm import get_llm

def analyze_impact_llm(
        text: str,
        npc_name: str,
        npc_personality: str,
) -> Dict[str, float]:
    """
    Analyze the impact of the player's text on the relationship using an LLM.
    Returns a dictionary with 'score_delta' and 'intensity'.
    """
    llm = get_llm()

    prompt = f"""
You are an AI analyzing a conversation in a game.
PLAYER: "{text}"
NPC: {npc_name} ({npc_personality})

Your task is to determine how this specific message affects the relationship between the Player and {npc_name}.

Rules:
1. If the player insults {npc_name}, the score should be negative (e.g., -5 to -10).
2. If the player compliments {npc_name}, the score should be positive (e.g., +2 to +5).
3. If the player insults *someone else* (e.g. "Eldon is stupid"), it should NOT negatively affect the relationship with {npc_name} significantly (maybe -1 or 0), unless {npc_name} is very loyal to them.
4. If the text is neutral, the score is 0.
5. "You are nice" or similar compliments are POSITIVE.

Output ONLY a single integer representing the change in relationship score (-10 to +10).
""".strip()

    try:
        response = llm.generate(prompt=prompt)
        # Attempt to parse integer
        import re
        match = re.search(r'-?\d+', response)
        if match:
            delta = int(match.group())
        else:
            delta = 0
    except Exception as e:
        print(f"DEBUG: Error in analyze_impact_llm: {e}")
        delta = 0

    # Clamp delta
    delta = max(-10, min(10, delta))

    return {
        "score_delta": delta,
        "intensity": abs(delta), # Use abs(delta) as proxy for emotional intensity
    }