from app.schemas.common import BaseSchema


class ChatRequest(BaseSchema):
    """
    Request schema for the AI chat endpoint.
    """

    message: str


class ChatResponse(BaseSchema):
    """
    Response returned by the AI chat endpoint.
    """

    response: str
    tool_name: str
    tool_output: dict