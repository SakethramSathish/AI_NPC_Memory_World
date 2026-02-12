from typing import Optional, List
from memory.chroma_client import ChromaClient
from graphs.state import MemoryContext
from config import MEMORY_TOP_K, MEMORY_IMPORTANCE_THRESHOLD

def _summarize_memories(memories: List[str]) -> str:
    """
    Deterministic summarization (NO LLM).
    Keeps memory explainable and cheap.
    """

    if not memories:
        return ""
    
    if len(memories) == 1:
        return memories[0]
    
    return " | ".join(memories[:3])

def retrieve_memory(
        npc_id: str,
        player_input: str,
) -> Optional[MemoryContext]:
    """
    Retrieve relevant memories for an NPC based on player input.
    Returns a MemoryContext or None.
    """

    collection_name = f"npc_memories_{npc_id}"
    collection = ChromaClient.get_collection(collection_name)

    try:
        results = collection.query(
            query_texts=[player_input],
            n_results=MEMORY_TOP_K,
            where={
                "importance": {"$gte": MEMORY_IMPORTANCE_THRESHOLD}
            },
        )

    except Exception:
        return None
    
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return None
    
    emotions = []
    trust_delta = 0
    source_types = []

    for meta in metadatas:
        if "emotion" in meta:
            emotions.append(meta["emotion"])
        if "impact_score" in meta:
            trust_delta += int(meta["impact_score"])
        if "source" in meta:
            source_types.append(meta["source"])

    dominant_emotion = max(set(emotions), key=emotions.count) if emotions else None

    memory_summary = _summarize_memories(documents)

    return MemoryContext(
        summary=memory_summary,
        dominant_emotion=dominant_emotion,
        trust_delta_estimate=trust_delta,
        source_types=list(set(source_types)),
    )