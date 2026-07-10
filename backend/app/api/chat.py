from fastapi import APIRouter

from app.graph.graph import graph
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):
    """
    Execute the LangGraph workflow for a user message.
    """

    state = {
        "message": request.message,
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    result = graph.invoke(state)

    return ChatResponse(
        response=result["response"],
        tool_name=result["tool_name"],
        tool_output=result["tool_output"],
    )