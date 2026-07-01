from langgraph.graph import END
from langgraph.graph import StateGraph

from agent.state import AgentState

from agent.nodes import (
    guardrail_node,
    intent_node,
    clarification_node,
    retriever_node,
    recommendation_node,
    comparison_node
)
builder = StateGraph(AgentState)

builder.add_node("guard", guardrail_node)
builder.add_node("intent", intent_node)
builder.add_node("clarify", clarification_node)
builder.add_node("retrieve", retriever_node)
builder.add_node("recommend", recommendation_node)
builder.add_node("compare", comparison_node)

builder.set_entry_point("guard")

builder.add_edge("guard", "intent")
def route(state):

    if state["end_of_conversation"]:
        return END

    if state["intent"] == "clarify":
        return "clarify"

    if state["intent"] == "compare":
        return "retrieve"

    return "retrieve"


builder.add_conditional_edges(
    "intent",
    route,
    {
        "clarify": "clarify",
        "retrieve": "retrieve",
        END: END
    }
)

def after_retrieval(state):

    if state["intent"] == "compare":
        return "compare"

    return "recommend"


builder.add_conditional_edges(
    "retrieve",
    after_retrieval,
    {
        "recommend": "recommend",
        "compare": "compare"
    }
)
builder.add_edge("clarify", END)
builder.add_edge("recommend", END)
builder.add_edge("compare", END)

graph = builder.compile()