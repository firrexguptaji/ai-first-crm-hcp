from __future__ import annotations

from datetime import date, datetime

from app.models.enums import InteractionChannel, Sentiment
from app.schemas.common import BaseSchema


class InteractionExtraction(BaseSchema):
    """
    Structured interaction information extracted by the LLM
    from a natural language conversation.

    This schema is used only by LangGraph tools and is
    independent of the database models.
    """

    hcp_name: str
    interaction_date: datetime
    channel: InteractionChannel
    raw_notes: str
    summary: str
    sentiment: Sentiment
    products_discussed: list[str] = []
    follow_up_required: bool = False
    follow_up_date: date | None = None