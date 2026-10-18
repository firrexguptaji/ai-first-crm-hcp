"""
Routing evaluation.

Live LLM evaluation (opt-in, calls Groq once per case):

    PowerShell:  $env:RUN_LLM_EVAL="1"; pytest tests/test_routing_eval.py -v
    bash:        RUN_LLM_EVAL=1 pytest tests/test_routing_eval.py -v

The keyword baseline runs on every test run and only checks that
the evaluation set itself is well formed.
"""

import os
import time

import pytest

from app.graph.registry import TOOLS
from app.graph.router import classify, llm_classify
from tests.routing_cases import ROUTING_CASES

RUN_LLM_EVAL = os.getenv("RUN_LLM_EVAL") == "1"

# Pause between live calls to stay under Groq rate limits.
EVAL_DELAY_SECONDS = float(os.getenv("LLM_EVAL_DELAY", "1.5"))


def test_routing_cases_use_registered_tools():
    for message, expected in ROUTING_CASES:
        assert expected in TOOLS, f"Unknown tool '{expected}' for: {message}"


def test_routing_cases_are_unique():
    messages = [message for message, _ in ROUTING_CASES]

    assert len(messages) == len(set(messages))


def test_keyword_baseline_report(capsys):
    """
    Not a pass/fail check: prints how the keyword fallback
    performs on the evaluation set, for comparison with the LLM.
    """

    misses = [
        (message, expected, classify(message))
        for message, expected in ROUTING_CASES
        if classify(message) != expected
    ]

    with capsys.disabled():
        total = len(ROUTING_CASES)
        print(
            f"\nKeyword baseline: {total - len(misses)}/{total} correct"
        )


@pytest.mark.skipif(
    not RUN_LLM_EVAL,
    reason="Live LLM evaluation is opt-in: set RUN_LLM_EVAL=1",
)
@pytest.mark.parametrize(("message", "expected"), ROUTING_CASES)
def test_llm_routing(message, expected):
    time.sleep(EVAL_DELAY_SECONDS)

    assert llm_classify(message) == expected
