from typing import TypedDict, List, Optional

#Player State

class PlayerState(TypedDict):
    """
    Represents the global player profile.
    This is NOT conversation history.
    """
    player_id: str
    reputation: int                         #Global reputation (-100 to +100)
    traits: List[str]                       #e.g. ["rude", "helpful", "honest"]


#NPC State

class NPCState(TypedDict):
    """
    Represents the current NPC being interacted with.
    """
    npc_id: str
    name: str
    personality: str                        #Fixed personality description
    mood: str                               #Dynamic: friendly / neutral / hostile
    relationship_score: int                 # -100 to +100

#Memory Context (Read-Only)

class MemoryContext(TypedDict):
    """
    Memory retrieved from Chroma for THIS interaction only.
    This is NOT persistent storage.
    """
    summary: str                            #Summarized relevant memory
    dominant_emotion: Optional[str]         #anger, trust, fear, etc.
    trust_delta_estimate: int               #Estimated effect on relationship
    source_types: List[str]                 #["direct", "gossip"]


#Interaction Context

class InteractionContext(TypedDict):
    """
    Represents the current turn.
    """
    player_input: str
    npc_response: Optional[str]
    timestamp: str                          #ISO formatted time

#Control Flag

class ControlFlags(TypedDict):
    """
    Used by LangGraph edges to control flow.
    """
    should_store_memory: bool
    should_gossip: bool
    memory_importance: float                #0.0 -> 1.0

#Final Graph State

class GraphState(TypedDict):
    """
    The ONLY state object that flows through LangGraph.
    """
    player: PlayerState
    npc: NPCState
    memory_context: Optional[MemoryContext]
    interaction: InteractionContext
    control: ControlFlags