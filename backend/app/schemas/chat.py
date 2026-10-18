from uuid import UUID

from pydantic import Field, field_validator

from app.schemas.common import BaseSchema


class ChatRequest(BaseSchema):
    """
    Request schema for the AI chat endpoint.

    Empty or oversized messages are rejected with HTTP 422
    before reaching the AI workflow.
    """

    message: str = Field(min_length=1, max_length=4000)

    # Interaction currently shown in the Interaction Details form.
    # Used to resolve edits such as "add Dr. Patel as an attendee".
    interaction_id: UUID | None = None

    @field_validator("message")
    @classmethod
    def strip_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message must not be empty.")

        return value


class ChatResponse(BaseSchema):
    """
    Response returned by the AI chat endpoint.
    """

    response: str
    tool_name: str
    tool_output: dict