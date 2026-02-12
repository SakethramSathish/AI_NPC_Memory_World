import streamlit as st
from datetime import datetime, timezone

from frontend.npc_selector import npc_selector, save_npc_profiles
from frontend.chat_ui import (
    init_chat,
    render_chat,
    chat_input,
    append_player_message,
    append_npc_message,
)
from frontend.npc_status_panel import render_npc_status
from frontend.gossip_log import render_gossip_log

from graphs.npc_interaction_graph import build_npc_interaction_graph
from graphs.state import GraphState
from utils.world_state import load_world_state
from config import GOSSIP_IMPORTANCE_THRESHOLD

#App Config

st.set_page_config(
    page_title="AI NPC Memory World",
    layout="wide",
)

st.title("🎮 AI NPCs That Remember You")

#Player Init

if "player_state" not in st.session_state:
    world_state = load_world_state()

    st.session_state.player_state = {
        "player_id": "player_001",
        "reputation": world_state.get("global_reputation", 0),
        "traits": [],
    }

#NPC Selection

selected_npc = npc_selector()

if not selected_npc:
    st.stop()

#Chat Init

init_chat()

#LangGraph Init

ALL_NPC_IDS = ["npc_eldon", "npc_mira"]
graph = build_npc_interaction_graph(ALL_NPC_IDS)

#Sidebar Panels

render_npc_status(selected_npc)
render_gossip_log(selected_npc["npc_id"])

#Chat Display

render_chat()
player_text = chat_input()

#Interaction Execution

if player_text:
    with st.chat_message("user"):
        st.write(player_text)
    append_player_message(player_text)

    append_player_message(player_text)

    #Tone and Importance Analysis
    
    from utils.text_analysis import analyze_impact_llm
    
    impact_analysis = analyze_impact_llm(
        text=player_text,
        npc_name=selected_npc["name"],
        npc_personality=selected_npc["personality"],
    )

    relationship_delta = impact_analysis["score_delta"]
    intensity = impact_analysis["intensity"]

    #Memory importance grows with emotional intensity
    # Using a slightly higher baseline since LLM intensity (0-10) is different from keyword counts
    memory_importance = min(1.0, 0.4 + (intensity * 0.1))

    #Build Initial Graph State

    state: GraphState = {
        "player": st.session_state.player_state,
        "npc": selected_npc,
        "memory_context": None,
        "interaction": {
            "player_input": player_text,
            "npc_response": None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "control":{
            "should_store_memory": True,
            "should_gossip": memory_importance >= GOSSIP_IMPORTANCE_THRESHOLD,
            "memory_importance": memory_importance,
        },
    }

    #Apply relationship delta BEFORE graph runs
    from utils.scoring import clamp
    new_score = clamp(state["npc"]["relationship_score"] + relationship_delta)
    state["npc"]["relationship_score"] = new_score
    print(f"DEBUG: Relationship delta: {relationship_delta}, New Score: {new_score}")

    #Run LangGraph

    final_state = graph.invoke(state)

    npc_reply = final_state["interaction"]["npc_response"]
    
    with st.chat_message("assistant"):
        st.write(npc_reply)
        
    append_npc_message(npc_reply)

    #Persist Updated States

    st.session_state.player_state = final_state["player"]
    selected_npc.update(final_state["npc"])
    save_npc_profiles()
    print(f"DEBUG: Saved profile for {selected_npc['name']} with Score: {selected_npc['relationship_score']}")