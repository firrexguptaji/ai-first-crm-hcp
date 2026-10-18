"""
History and search tools against a real database (#81, P1).
"""

from datetime import datetime

import pytest

from app.graph.tools import interaction_history as history_tool
from app.graph.tools import search_hcp as search_tool
from app.schemas.ai import HCPSearchExtraction, InteractionHistoryExtraction

pytestmark = pytest.mark.db


def state(message):
    return {"message": message, "tool_name": "", "tool_input": {},
            "tool_output": {}, "response": "", "context": {}}


def test_history_returns_only_that_hcp_newest_first(
    monkeypatch, create_hcp, create_db_interaction,
):
    hcp = create_hcp()
    other = create_hcp()
    old = create_db_interaction(hcp, interaction_date=datetime(2026, 9, 1, 9))
    new = create_db_interaction(hcp, interaction_date=datetime(2026, 10, 1, 9))
    create_db_interaction(other)

    name = f"{hcp.first_name} {hcp.last_name}"
    monkeypatch.setattr(history_tool, "extract_history",
                        lambda m: InteractionHistoryExtraction(hcp_name=name))

    output = history_tool.interaction_history(state(f"Show history for {name}"))["tool_output"]

    assert [r["id"] for r in output["results"]] == [str(new.id), str(old.id)]


def test_history_for_unknown_hcp_raises(monkeypatch):
    monkeypatch.setattr(history_tool, "extract_history",
                        lambda m: InteractionHistoryExtraction(hcp_name="Nobody Zzqx"))

    with pytest.raises(ValueError, match="not found"):
        history_tool.interaction_history(state("Show history for Nobody Zzqx"))


def test_search_by_specialization(monkeypatch, create_hcp):
    target = create_hcp(specialization="Zzqxology")
    create_hcp(specialization="Cardiology")

    monkeypatch.setattr(search_tool, "extract_search",
                        lambda m: HCPSearchExtraction(specialization="Zzqxology"))

    output = search_tool.search_hcp(state("Find Zzqxology doctors"))["tool_output"]

    assert [r["id"] for r in output["results"]] == [str(target.id)]
