from .mongo import notes_collection, wishlist_collection, saving_collection
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import ReturnDocument

# NOTES
def add_note(user_id: int, note_type: str, amount: int, desc: str):
    doc = {
        "user_id": int(user_id),
        "type": note_type,  # "income" or "expense"
        "amount": int(amount),
        "desc": desc,
        "created_at": datetime.utcnow()
    }
    res = notes_collection.insert_one(doc)
    return str(res.inserted_id)

def get_notes(user_id: int, filters=None, limit=200):
    q = {"user_id": int(user_id)}
    if filters:
        q.update(filters)
    return list(notes_collection.find(q).sort("created_at", -1).limit(limit))

def sum_balance(user_id: int):
    pipeline = [
        {"$match": {"user_id": int(user_id)}},
        {"$group": {
            "_id": "$type",
            "total": {"$sum": "$amount"}
        }}
    ]
    res = list(notes_collection.aggregate(pipeline))
    total = 0
    for r in res:
        if r["_id"] == "income":
            total += r["total"]
        elif r["_id"] == "expense":
            total -= r["total"]
    return total

def delete_note_by_id(user_id: int, note_id: str):
    try:
        res = notes_collection.delete_one({"_id": ObjectId(note_id), "user_id": int(user_id)})
        return res.deleted_count == 1
    except Exception:
        return False

# WISHLIST
def add_wishlist(user_id: int, name: str, target_price: int):
    doc = {
        "user_id": int(user_id),
        "name": name,
        "target_price": int(target_price),
        "saved": 0,
        "status": "active",
        "created_at": datetime.utcnow()
    }
    r = wishlist_collection.insert_one(doc)
    return str(r.inserted_id)

def get_wishlist(user_id: int):
    return list(wishlist_collection.find({"user_id": int(user_id)}).sort("created_at", -1))

def delete_wishlist_by_name(user_id: int, name: str):
    res = wishlist_collection.delete_one({"user_id": int(user_id), "name": name})
    return res.deleted_count == 1

def update_wishlist_saved(user_id: int, wish_id: str, amount: int):
    try:
        _id = ObjectId(wish_id)
    except Exception:
        return False
    res = wishlist_collection.find_one_and_update(
        {"_id": _id, "user_id": int(user_id)},
        {"$inc": {"saved": int(amount)}},
        return_document=ReturnDocument.AFTER
    )
    return res is not None

def set_wishlist_status(user_id: int, wish_id: str, status: str):
    try:
        _id = ObjectId(wish_id)
    except Exception:
        return False
    res = wishlist_collection.update_one({"_id": _id, "user_id": int(user_id)}, {"$set": {"status": status}})
    return res.modified_count == 1

# SAVING
def add_saving_record(user_id: int, tujuan: str, amount: int):
    doc = {
        "user_id": int(user_id),
        "tujuan": tujuan,  # "general" or wishlist_id
        "amount": int(amount),
        "created_at": datetime.utcnow()
    }
    r = saving_collection.insert_one(doc)
    return str(r.inserted_id)

def get_saving_history(user_id: int, limit=100):
    return list(saving_collection.find({"user_id": int(user_id)}).sort("created_at", -1).limit(limit))
