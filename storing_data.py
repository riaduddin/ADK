from pymongo import MongoClient

import os

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)
db = client["engineering_components"]


def get_component_from_db(collection_name, user_id, session_id):
    collection = db[collection_name]
    result = collection.find_one({"user_id": user_id, "session_id": session_id})
    if result:
        return result.get("data", {})
    else:
        raise HTTPException(status_code=404, detail=f"{collection_name} not found for given user and session.")


def store_component_in_db(collection_name, component_data, user_id, session_id):
    collection = db[collection_name]
    doc = {
        "user_id": user_id,
        "session_id": session_id,
        "data": component_data
    }
    result = collection.insert_one(doc)
    print(f"📥 Stored in '{collection_name}' with _id: {result.inserted_id}")