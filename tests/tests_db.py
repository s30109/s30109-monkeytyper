import pytest
from database.db import client, users_collection, scores_collection
from database.models import (
    get_or_create_user,
    get_user_scores,
    insert_score,
    get_top_scores
)
from pymongo.errors import ServerSelectionTimeoutError

# === FIXTURE ===

@pytest.fixture
def mongo_connection():
    try:
        client.admin.command("ping")
    except ServerSelectionTimeoutError:
        pytest.skip("MongoDB not running on localhost:27017")

@pytest.fixture
def test_user(mongo_connection):
    username = "test_user"
    users_collection.delete_many({"username": username})
    scores_collection.delete_many({"username": username})
    user_id = get_or_create_user(username)
    return user_id, username

# === TESTY ===

def test_database_connection(mongo_connection):
    try:
        result = client.admin.command("ping")
        assert result["ok"] == 1.0
    except Exception as e:
        pytest.fail(f"Połączenie z MongoDB nieudane: {e}")

def test_create_and_get_user(mongo_connection, test_user):
    user_id, username = test_user
    user = users_collection.find_one({"username": username})
    assert user is not None
    assert user["username"] == username

def test_get_nonexistent_user(mongo_connection):
    user = users_collection.find_one({"username": "nick_ktorego_nie_ma"})
    assert user is None

def test_insert_score_success(mongo_connection, test_user):
    user_id, username = test_user
    result = {
        "wpm": 80,
        "accuracy": 95.0,
        "correct": 28,
        "total_words": 30
    }
    insert_score(user_id, username, result)
    inserted = scores_collection.find_one({"username": username})
    assert inserted is not None
    assert inserted["wpm"] == 80

def test_insert_score_multiple(mongo_connection, test_user):
    user_id, username = test_user
    insert_score(user_id, username, {
        "wpm": 50, "accuracy": 85.0, "correct": 20, "total_words": 25
    })
    insert_score(user_id, username, {
        "wpm": 75, "accuracy": 90.0, "correct": 22, "total_words": 25
    })
    results = list(scores_collection.find({"username": username}))
    assert len(results) >= 2

def test_get_user_scores_returns_list(mongo_connection, test_user):
    user_id, username = test_user
    scores = get_user_scores(username)
    assert isinstance(scores, list)
    assert all(score["username"] == username for score in scores)

def test_get_top_scores_limit(mongo_connection):
    top = get_top_scores()
    assert isinstance(top, list)
    assert len(top) <= 10
