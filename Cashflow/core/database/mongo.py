from pymongo import MongoClient
from config import MONGO_URL, NAMA_DB

client = MongoClient(MONGO_URL)
db = client[NAMA_DB]

notes_collection = db["notes"]
wishlist_collection = db["wishlist"]
saving_collection = db["savings"]

def init_db():
    # useful indexes for queries
    try:
        notes_collection.create_index([("user_id", 1)])
        notes_collection.create_index([("created_at", -1)])
        wishlist_collection.create_index([("user_id", 1), ("name", 1)])
        saving_collection.create_index([("user_id", 1), ("created_at", -1)])
    except Exception as e:
        print("Init DB index warning:", e)
