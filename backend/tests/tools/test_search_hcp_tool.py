from app.graph.tools.search_hcp import search_hcp


def test_search_hcp_returns_results(monkeypatch):
    class FakeExtraction:
        name = "Alice"
        specialization = None
        organization = None

        def model_dump(self):
            return {
                "name": "Alice",
                "specialization": None,
                "organization": None,
            }

    class FakeHCP:
        id = "123"
        first_name = "Alice"
        last_name = "Brown"
        specialization = "Cardiology"
        organization = "Apollo Hospital"

    def fake_extract(message):
        return FakeExtraction()

    def fake_search(extraction):
        return [FakeHCP()]

    monkeypatch.setattr(
        "app.graph.tools.search_hcp.extract_search",
        fake_extract,
    )

    monkeypatch.setattr(
        "app.graph.tools.search_hcp.search_hcp_records",
        fake_search,
    )

    state = {
        "message": "Find Dr. Alice Brown",
        "tool_name": "search_hcp",
        "tool_input": {},
        "tool_output": {},
        "response": "",
    }

    result = search_hcp(state)

    assert result["tool_output"]["success"] is True
    assert result["tool_output"]["count"] == 1
    assert result["tool_output"]["results"][0]["first_name"] == "Alice"
    assert result["response"] == "Found 1 Healthcare Professional(s)."