import random
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from engine.core import get_random_words, evaluate_typing
from database.models import get_or_create_user, insert_score, get_top_scores, get_user_scores

UI_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ui"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_PATH = os.path.join(BASE_DIR, "..", "words.txt")

app = Flask(__name__)
CORS(app)

# Wczytaj słowa z pliku
with open(WORDS_PATH, "r", encoding="utf-8") as f:
    WORDS = [line.strip() for line in f if line.strip()]

@app.route("/api/game/words", methods=["GET"])
def get_words():
    """Zwraca 30 losowych słów do przepisania."""
    return jsonify({"words": get_random_words(WORDS, count=30)})

@app.route("/api/game/submit", methods=["POST"])
def submit_score():
    """Odbiera dane z gry i zapisuje wynik użytkownika."""
    data = request.json
    username = data.get("username")
    typed_words = data.get("typed_words", [])
    expected_words = data.get("expected_words", [])
    time_taken = data.get("time", 30)

    result = evaluate_typing(typed_words, expected_words, time_taken)
    result["username"] = username

    user_id = get_or_create_user(username)
    insert_score(user_id, username, result)

    return jsonify(result)

@app.route("/api/highscores", methods=["GET"])
def api_highscores():
    """Zwraca 10 najlepszych wyników."""
    scores = get_top_scores()
    return jsonify([{
        "username": s["username"],
        "wpm": s["wpm"],
        "accuracy": s["accuracy"]
    } for s in scores])

@app.route("/api/highscores/user", methods=["GET"])
def api_user_highscores():
    """Zwraca 10 najlepszych wyników danego użytkownika."""
    username = request.args.get("username")
    if not username:
        return jsonify([])
    scores = get_user_scores(username)
    return jsonify([{
        "username": s["username"],
        "wpm": s["wpm"],
        "accuracy": s["accuracy"]
    } for s in scores])

@app.route("/", methods=["GET"])
def serve_index():
    return send_from_directory(UI_FOLDER, "index.html")

@app.route("/<path:filename>", methods=["GET"])
def serve_static(filename):
    return send_from_directory(UI_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
