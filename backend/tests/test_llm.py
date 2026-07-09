from app.llm.groq import llm


def test_llm():
    response = llm.invoke("Say hello in one sentence.")

    assert response.content
    print(response.content)