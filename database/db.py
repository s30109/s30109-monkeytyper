from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Test połączenia
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["typinggame"]
    users_collection = db["users"]
    scores_collection = db["scores"]
    client.admin.command("ping")
    print("✅ Połączono z MongoDB.")
except Exception as e:
    print("❌ Błąd połączenia z MongoDB:", e)


