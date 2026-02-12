from graphs.npc_interaction_graph import build_npc_interaction_graph


def test_graph_runs():
    graph = build_npc_interaction_graph(["npc_a", "npc_b"])

    state = {
        "player": {
            "player_id": "player_test",
            "reputation": 0,
            "traits": [],
        },
        "npc": {
            "npc_id": "npc_a",
            "name": "NPC A",
            "personality": "grumpy",
            "mood": "neutral",
            "relationship_score": 0,
        },
        "memory_context": None,
        "interaction": {
            "player_input": "Hello",
            "npc_response": None,
            "timestamp": "2025-01-01T00:00:00",
        },
        "control": {
            "should_store_memory": False,
            "should_gossip": False,
            "memory_importance": 0.5,
        },
    }

    result = graph.invoke(state)

    assert result["interaction"]["npc_response"] is not None
