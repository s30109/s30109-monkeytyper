import pytest
import json
from api.api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_game_returns_words(client):
    response = client.get("/api/game/words")  # zmieniono ścieżkę
    assert response.status_code == 200
    data = response.get_json()
    assert "words" in data
    assert isinstance(data["words"], list)
    assert len(data["words"]) == 30

def test_submit_returns_score(client):
    payload = {
        "username": "test_user",
        "typed_words": ["apple", "banana", "cherry"],
        "expected_words": ["apple", "banana", "cherry"],
        "time": 30
    }
    response = client.post("/api/game/submit", data=json.dumps(payload),  # zmieniono ścieżkę
                           content_type="application/json")
    assert response.status_code == 200
    result = response.get_json()
    assert result["username"] == "test_user"
    assert result["correct"] == 3
    assert result["accuracy"] == 100.0
    assert "wpm" in result
