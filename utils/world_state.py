import json
from pathlib import Path
from typing import Dict, Any

WORLD_STATE_PATH = Path("data/world_state.json")

def load_world_state() -> Dict[str, Any]:
    """
    Load the global world state from disk.
    """

    if not WORLD_STATE_PATH.exists():
        return {
            "global_reputation": 0,
            "world_events": [],
        }
    
    with open (WORLD_STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_world_state(state: Dict[str, Any]) -> None:
    """
    Persist the global world state to disk.
    """

    WORLD_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(WORLD_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def update_global_reputation(delta: int) -> Dict[str, Any]:
    """
    Update global reputation and persist it.
    """
    state = load_world_state()
    state["global_reputation"] += delta
    state["global_reputation"] = max(-100, min(100, state["global_reputation"]))

    save_world_state(state)
    return state

def add_world_event(event: str) -> Dict[str, Any]:
    """
    Add a world-level event (optional future use).
    """
    state = load_world_state()
    state["world_events"].append(event)
    save_world_state(state)
    return state