from __future__ import annotations

from typing import TypeVar

from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq
from pydantic import BaseModel

from app.config.settings import settings

T = TypeVar("T", bound=BaseModel)

llm = ChatGroq(
    model=settings.model_name,
    api_key=settings.groq_api_key,
    temperature=0,
)


def structured(schema: type[T]) -> Runnable:
    """
    Return the LLM bound to a Pydantic schema.

    Uses Groq's JSON-schema response format instead of forced tool
    calling. Reasoning models such as openai/gpt-oss-120b sometimes
    answer in prose when a tool call is required, which Groq rejects
    with "Tool choice is required, but model did not call a tool".
    A JSON-schema response format constrains the output directly.
    """

    return llm.with_structured_output(
        schema,
        method="json_schema",
    )
