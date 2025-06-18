from database.db import users_collection, scores_collection
from bson import ObjectId
from datetime import datetime

def get_or_create_user(username):
    user = users_collection.find_one({"username": username})
    if user:
        return user["_id"]
    return users_collection.insert_one({"username": username}).inserted_id

def insert_score(user_id, username, result):
    scores_collection.insert_one({
        "user_id": ObjectId(user_id),
        "username": username,
        "wpm": result["wpm"],
        "accuracy": result["accuracy"],
        "correct": result["correct"],
        "total_words": result["total_words"],
        "date": datetime.utcnow()
    })

def get_top_scores(limit=10):
    return list(scores_collection.find().sort("wpm", -1).limit(limit))

def get_user_scores(username, limit=10):
    return list(scores_collection.find({"username": username}).sort("wpm", -1).limit(limit))