from graphs.state import GraphState


def should_gossip(state: GraphState) -> bool:
    """
    Decide whether gossip should be triggered.
    """
    return state["control"].get("should_gossip", False)


def should_summarize(state: GraphState) -> bool:
    """
    Decide whether memory summarization should run.
    This is always true at the end of an interaction,
    but kept as a function for future flexibility.
    """
    return True
