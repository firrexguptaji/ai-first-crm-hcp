import logging

from fastapi import APIRouter

from app.graph.graph import GENERIC_ERROR_MESSAGE, graph
from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

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

    Tool errors are handled inside the graph. This endpoint only
    catches failures outside the tools (e.g. routing), so the
    frontend always receives a ChatResponse.
    """

    state = {
        "message": request.message,
        "tool_name": "",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    try:
        result = graph.invoke(state)

    except Exception:
        logger.exception("Chat workflow failed for message: %s", request.message)

        return ChatResponse(
            response=GENERIC_ERROR_MESSAGE,
            tool_name="",
            tool_output={
                "success": False,
                "error_type": "internal",
                "error": GENERIC_ERROR_MESSAGE,
            },
        )

    return ChatResponse(
        response=result["response"],
        tool_name=result["tool_name"],
        tool_output=result["tool_output"],
    )
