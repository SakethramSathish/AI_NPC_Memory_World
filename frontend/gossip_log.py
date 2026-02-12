import streamlit as st

from memory.gossip_memory import retrieve_gossip

def render_gossip_log(npc_id: str):
    """
    Display gossip known to the selected NPC.
    """

    st.sidebar.markdown("## 🗣️ Gossip Log")

    gossip_items = retrieve_gossip(npc_id)

    if not gossip_items:
        st.sidebar.caption("No gossip yet.")
        return
    
    for gossip in gossip_items:
        st.sidebar.markdown(f"• {gossip}")