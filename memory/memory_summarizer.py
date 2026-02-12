from typing import List
from datetime import datetime,timezone
from memory.chroma_client import ChromaClient
from config import MEMORY_SUMMARIZATION_INTERVAL

def summarize_memories(
        npc_id: str,
        recent_limit: int = MEMORY_SUMMARIZATION_INTERVAL,
):
    """
    Summarize recent memories for an NPC into a single high-level memory.
    This is deterministic and does NOT use an LLM.
    """

    collection_name = f"npc_memories_{npc_id}"
    collection = ChromaClient.get_collection(collection_name)

    try:
        results = collection.get(
            limit = recent_limit,
            include = ["documents", "metadatas", "ids"],
        )

    except Exception:
        return
    
    documents: List[str] = results.get("documents", [])
    metadatas: List[dict] = results.get("metadatas", [])
    ids: List[str] = results.get("ids", [])

    if len(documents) < recent_limit:
        #Not enough memories to summarize yet
        return
    
    #Create Summary

    summary_text = "Repeated interactions indicate: "
    summary_text += " | ".join(documents[:3])

    summary_metadata = {
        "npc_id": npc_id,
        "emotion": _dominant_emotion(metadatas),
        "impact_score": _total_impact(metadatas),
        "importance": 0.9,
        "source": "summary",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    summary_id = f"{npc_id}_summary_{summary_metadata['timestamp']}"

    #Store summarized memory

    collection.add(
        documents = [summary_text],
        metadatas = [summary_metadata],
        ids = [summary_id],
    )

    #Clean Up old memories

    collection.delete(id = ids)

def _dominant_emotion(metadatas: List[dict]) -> str:
    """
    Determine dominant emotion from a list of metadata entries.
    """
    emotions = [m.get("emotion") for m in metadatas if m.get("emotion")]
    if not emotions:
        return "neutral"
    return max(set(emotions), key=emotions.count)

def _total_impact(metadatas: List[dict]) -> int:
    """
    Aggregate relationship impact.
    """
    return sum(int(m.get("impact_score", 0)) for m in metadatas)