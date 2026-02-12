from memory.gossip_memory import store_gossip, retrieve_gossip


def test_gossip_flow():
    store_gossip(
        target_npc_id="npc_target",
        source_npc_id="npc_source",
        content="Player cheated someone.",
        emotion="distrust",
        confidence=0.9,
    )

    gossip = retrieve_gossip("npc_target")

    assert len(gossip) > 0
    assert "cheated" in gossip[0].lower()
