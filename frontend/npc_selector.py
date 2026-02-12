import json
import streamlit as st
from pathlib import Path

NPC_PROFILE_PATH = Path("data/npc_profiles.json")

def load_npc_profiles():
    """
    Load NPC profiles from JSON into Session State if not present.
    """
    if "npc_profiles" not in st.session_state:
        if not NPC_PROFILE_PATH.exists():
            st.error("NPC profiles not found.")
            st.session_state.npc_profiles = []
            return

        with open(NPC_PROFILE_PATH, "r", encoding="utf-8") as f:
            st.session_state.npc_profiles = json.load(f)

def save_npc_profiles():
    """
    Save current NPC profiles from Session State to JSON.
    """
    if "npc_profiles" in st.session_state:
        with open(NPC_PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(st.session_state.npc_profiles, f, indent=2)

def npc_selector():
    """
    Streamlit UI to select an NPC.
    Returns the selected NPC dictionary from Session State.
    """
    st.sidebar.header("🎭 Choose an NPC")

    load_npc_profiles()
    
    if not st.session_state.npc_profiles:
        return None
    
    npc_names = [npc["name"] for npc in st.session_state.npc_profiles]

    selected_name = st.sidebar.selectbox(
        "Who do you want to talk to?",
        npc_names,
    )

    # Return the MUTABLE reference from session state
    selected_npc = next(
        npc for npc in st.session_state.npc_profiles if npc["name"] == selected_name
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Personality:** {selected_npc['personality']}")
    st.sidebar.markdown(f"**Default Mood:** {selected_npc.get('mood', 'neutral')}")

    return selected_npc