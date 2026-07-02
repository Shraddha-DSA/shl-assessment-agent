from fastapi import FastAPI

from app.schemas import ChatRequest, ChatResponse
from agent.graph import graph

app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0.0"
)
@app.get("/health")
def health():
    return {
        "status": "ok"
    }
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    user_query = request.messages[-1].content

    state = {
        "messages": [m.model_dump() for m in request.messages],
        "user_query": user_query,
        "intent": "",
        "retrieved_docs": [],
        "recommendations": [],
        "reply": "",
        "needs_clarification": False,
        "end_of_conversation": False
    }

    result = graph.invoke(state)

    return ChatResponse(
        reply=result["reply"],
        recommendations=result.get("recommendations", []),
        end_of_conversation=result["end_of_conversation"]
    )