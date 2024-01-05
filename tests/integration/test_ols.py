import requests
from fastapi.testclient import TestClient

from app.endpoints import ols
from app.main import app

client = TestClient(app)


def test_healthz() -> None:
    response = client.get("/healthz")
    assert response.status_code == requests.codes.ok
    assert response.json() == {"status": "1"}


def test_readyz() -> None:
    response = client.get("/readyz")
    assert response.status_code == requests.codes.ok
    assert response.json() == {"status": "1"}


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == requests.codes.ok
    assert response.json() == {
        "message": "This is the default endpoint for OLS",
        "status": "running",
    }


def test_status() -> None:
    response = client.get("/status")
    assert response.status_code == requests.codes.ok
    assert response.json() == {
        "message": "This is the default endpoint for OLS",
        "status": "running",
    }


def test_raw_prompt(monkeypatch) -> None:
    # the raw prompt should just return stuff from LangChainInterface, so mock that base method
    # model_context is what imports LangChainInterface, so we have to mock that particular usage/"instance"
    # of it in our tests

    from tests.mock_classes.langchain_interface import mock_langchain_interface
    from tests.mock_classes.llm_loader import mock_llm_loader

    ml = mock_langchain_interface("test response")

    monkeypatch.setattr(ols, "LLMLoader", mock_llm_loader(ml()))

    response = client.post(
        "/ols/raw_prompt", json={"conversation_id": "1234", "query": "test query"}
    )
    print(response)
    assert response.status_code == requests.codes.ok
    assert response.json() == {
        "conversation_id": "1234",
        "query": "test query",
        "response": "test response",
    }
