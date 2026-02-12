from typing import List
from datetime import datetime, timezone
from memory.chroma_client import ChromaClient

def store_gossip(
        target_npc_id: str,
        source_npc_id: str,
        content: str,
        emotion: str,
        confidence: float,
):
    
    """
    Store gossip ABOUT the player in another NPC's gossip memory.
    """

    collection = ChromaClient.get_collection(f"npc_gossip_{target_npc_id}")

    metadata = {
        "source_npc": source_npc_id,
        "emotion": emotion,
        "confidence": confidence,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "gossip",
    }

    gossip_id = f"gossip_{source_npc_id}_{metadata['timestamp']}"

    print(f"DEBUG: Storing gossip for {target_npc_id} from {source_npc_id}: {content}")
    collection.add(
        documents = [content],
        metadatas = [metadata],
        ids = [gossip_id],
    )

def retrieve_gossip(npc_id: str) -> List[str]:
    """
    Retrieve gossip memories for an NPC.
    Returns the 10 most recent gossip items.
    """

    collection = ChromaClient.get_collection(f"npc_gossip_{npc_id}")

    try: 
        # Fetch up to 20 raw items
        results = collection.get(limit=20)
    except Exception as e:
        print(f"DEBUG: Error retrieving gossip: {e}")
        return []
    
    if not results or not results["documents"]:
        return []

    # Zip documents and metadatas together
    documents = results["documents"]
    metadatas = results["metadatas"]
    
    # Create a list of tuples: (timestamp, content, source_npc)
    gossip_list = []
    for doc, meta in zip(documents, metadatas):
        # Handle cases where meta might be None
        if not meta: 
            continue
        timestamp = meta.get("timestamp", "")
        source = meta.get("source_npc", "Unknown")
        gossip_list.append((timestamp, doc, source))

    # Sort by timestamp descending (newest first)
    gossip_list.sort(key=lambda x: x[0], reverse=True)

    # Format the top 10
    formatted_gossip = []
    for _, content, source in gossip_list[:10]:
        formatted_gossip.append(f"**{source}**: {content}")

    return formatted_gossip
        
    