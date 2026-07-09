from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.llm.groq import llm


class GraphState(TypedDict):
    message: str


def chat_node(state: GraphState):
    response = llm.invoke(state["message"])

    return {
        "message": response.content,
    }


builder = StateGraph(GraphState)

builder.add_node("chat", chat_node)

builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile()