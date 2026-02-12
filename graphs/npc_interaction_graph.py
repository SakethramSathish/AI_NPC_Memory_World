from langgraph.graph import StateGraph, END
from graphs.state import GraphState
from graphs.nodes import (
    init_timestamp_node,
    memory_retrieve_node,
    emotion_update_node,
    dialogue_node,
    memory_store_node,
    world_update_node,
    gossip_node,
    memory_summarization_node,
)
from graphs.edges import should_gossip
from config import MEMORY_SUMMARIZATION_INTERVAL

def build_npc_interaction_graph(all_npc_ids):
    """
    Build and return the LangGraph for NPC interactions.
    """

    graph = StateGraph(GraphState)

    #Add Nodes

    graph.add_node("init_timestamp", init_timestamp_node)
    graph.add_node("retrieve_memory", memory_retrieve_node)
    graph.add_node("update_emotion", emotion_update_node)
    graph.add_node("dialogue", dialogue_node)
    graph.add_node("store_memory", memory_store_node)
    graph.add_node("update_world", world_update_node)
    graph.add_node(
        "spread_gossip",
        lambda state: gossip_node(state, all_npc_ids)
    )
    graph.add_node("summarize_memory", memory_summarization_node)

    #Define Edges (Flow)

    graph.set_entry_point("init_timestamp")

    graph.add_edge("init_timestamp", "retrieve_memory")
    graph.add_edge("retrieve_memory", "update_emotion")
    graph.add_edge("update_emotion", "dialogue")
    graph.add_edge("dialogue", "store_memory")
    graph.add_edge("store_memory", "update_world")    
    graph.add_conditional_edges(
        "update_world",
        should_gossip,
        {
            True: "spread_gossip",
            False: "summarize_memory",
        },
    )
    graph.add_edge("spread_gossip", "summarize_memory")

    #Summarization -> END

    graph.add_edge("summarize_memory", END)

    return graph.compile()