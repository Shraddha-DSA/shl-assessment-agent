from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    messages: List[Dict[str, str]]

    user_query: str

    intent: str

    retrieved_docs: List[Dict[str, Any]]

    recommendations: List[Dict[str, Any]]

    reply: str

    end_of_conversation: bool

    needs_clarification: bool