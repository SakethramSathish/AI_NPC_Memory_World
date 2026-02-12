from datetime import datetime, timezone
from graphs.state import GraphState
from memory.memory_retriever import retrieve_memory
from memory.memory_writer import store_memory
from memory.memory_summarizer import summarize_memories
from agents.emotion_agent import update_emotion
from agents.npc_agent import generate_npc_response
from agents.world_agent import update_world_state
from agents.gossip_agent import spread_gossip
from config import MEMORY_SUMMARIZATION_INTERVAL

#Memory Retrieval Node

def memory_retrieve_node(state: GraphState) -> GraphState:
    npc_id = state["npc"]["npc_id"]
    player_input = state["interaction"]["player_input"]

    memory_context = retrieve_memory(
        npc_id=npc_id,
        player_input=player_input
    )

    state["memory_context"] = memory_context
    return state

#Emotion Update Node

def emotion_update_node(state: GraphState) -> GraphState:
    return update_emotion(state)

#Dialogue Node

def dialogue_node(state: GraphState) -> GraphState:
    return generate_npc_response(state)

#Memory Store Node

def memory_store_node(state: GraphState) -> GraphState:
    return store_memory(state)

#World Update Node

def world_update_node(state: GraphState) -> GraphState:
    return update_world_state(state)

#Gossip Node

def gossip_node(state: GraphState, all_npc_ids) -> GraphState:
    return spread_gossip(state, all_npc_ids)

#Memory Summarization

def memory_summarization_node(state: GraphState) -> GraphState:
    """
    Periodically compress memory to prevent explosion.
    """

    npc_id = state["npc"]["npc_id"]

    summarize_memories(npc_id)
    return state

#Timestamp Init

def init_timestamp_node(state: GraphState) -> GraphState:
    state["interaction"]["timestamp"] = datetime.now(timezone.utc).isoformat()
    return state