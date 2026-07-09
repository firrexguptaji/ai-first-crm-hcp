from enum import Enum


class InteractionChannel(str, Enum):
    """Supported interaction channels."""

    IN_PERSON = "IN_PERSON"
    PHONE = "PHONE"
    EMAIL = "EMAIL"
    VIDEO = "VIDEO"
    OTHER = "OTHER"


class Sentiment(str, Enum):
    """Interaction sentiment."""

    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"