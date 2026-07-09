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
    
    
class InteractionUpdateExtraction(BaseSchema):
    """
    Structured interaction update extracted by the LLM.

    Only the fields that should be updated are populated.
    """

    hcp_name: str
    interaction_id: str | None = None

    interaction_date: datetime | None = None
    channel: InteractionChannel | None = None
    raw_notes: str | None = None
    summary: str | None = None
    sentiment: Sentiment | None = None
    products_discussed: list[str] | None = None
    follow_up_required: bool | None = None
    follow_up_date: date | None = None
    
    
class HCPSearchExtraction(BaseSchema):
    """
    Structured Healthcare Professional search request
    extracted from natural language.
    """

    name: str | None = None
    specialization: str | None = None
    organization: str | None = None
    
class InteractionHistoryExtraction(BaseSchema):
    """
    Structured interaction history request extracted
    from natural language.
    """

    hcp_name: str
    limit: int | None = None
    
class FollowUpExtraction(BaseSchema):
    """
    Structured follow-up request extracted
    from natural language.
    """

    hcp_name: str

class FollowUpRecommendation(BaseSchema):
    """
    AI-generated follow-up recommendation.
    """

    recommendation: str
    rationale: str