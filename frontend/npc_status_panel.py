import streamlit as st

def render_npc_status(npc_state: dict):
    """
    Display NPC mood and relationship status.
    """

    if not npc_state:
        return
    
    st.sidebar.markdown("## 🎭 NPC Status")

    mood = npc_state.get("mood", "neutral")
    relationship = npc_state.get("relationship_score", 0)

    # Mood display
    mood_color = {
        "friendly": "🟢",
        "neutral": "🟡",
        "hostile": "🔴",
    }.get(mood, "⚪")

    st.sidebar.markdown(f"**Mood:** {mood_color} {mood.capitalize()}")

    #Relationship Bar
    from utils.scoring import get_relationship_status
    status_text = get_relationship_status(relationship)
    
    st.sidebar.markdown(f"**Relationship:** {status_text} ({relationship})")
    st.sidebar.progress((relationship + 100) / 200)