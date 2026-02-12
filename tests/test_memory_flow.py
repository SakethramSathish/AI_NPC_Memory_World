from memory.memory_writer import store_memory
from memory.memory_retriever import retrieve_memory
from graphs.state import GraphState


def test_memory_write_and_retrieve():
    state: GraphState = {
        "player": {
            "player_id": "test_player",
            "reputation": 0,
            "traits": [],
        },
        "npc": {
            "npc_id": "npc_test",
            "name": "Test NPC",
            "personality": "neutral",
            "mood": "neutral",
            "relationship_score": 0,
        },
        "memory_context": None,
        "interaction": {
            "player_input": "You are annoying",
            "npc_response": "That's rude.",
            "timestamp": "2025-01-01T00:00:00",
        },
        "control": {
            "should_store_memory": True,
            "should_gossip": False,
            "memory_importance": 0.9,
        },
    }

    store_memory(state)

    memory = retrieve_memory(
        npc_id="npc_test",
        player_input="annoying",
    )

    assert memory is not None
    assert "annoying" in memory["summary"].lower()
