from datetime import datetime, timezone

from bson.objectid import ObjectId

from mongo_client import chats_collection


def normalize_gender(gender):
    """Normalize incoming gender values for consistent prompt selection."""
    if not gender:
        return None

    normalized = gender.strip().lower()
    return normalized if normalized in {"male", "female"} else None


def _build_chat_lookup(chat_id):
    if ObjectId.is_valid(chat_id):
        return {"$or": [{"_id": ObjectId(chat_id)}, {"external_chat_id": chat_id}]}
    return {"external_chat_id": chat_id}


def get_chat(chat_id):
    """Fetch a chat document by Mongo ObjectId or external chat id."""
    return chats_collection.find_one(_build_chat_lookup(chat_id))


def upsert_chat(chat_id, gender=None):
    """Create or update chat metadata using the incoming chat id."""
    existing_chat = get_chat(chat_id)
    normalized_gender = normalize_gender(gender)
    update_fields = {
        "updated_at": datetime.now(timezone.utc),
    }

    if normalized_gender is not None:
        update_fields["gender"] = normalized_gender

    if existing_chat:
        chats_collection.update_one({"_id": existing_chat["_id"]}, {"$set": update_fields})
        return chats_collection.find_one({"_id": existing_chat["_id"]})

    chat_doc = {
        "external_chat_id": chat_id,
        "gender": normalized_gender,
        "created_at": datetime.now(timezone.utc),
        **update_fields,
    }
    result = chats_collection.insert_one(chat_doc)
    return chats_collection.find_one({"_id": result.inserted_id})


def get_chat_gender(chat_id):
    """Get the gender associated with a chat."""
    chat = get_chat(chat_id)
    return chat.get("gender") if chat else None
