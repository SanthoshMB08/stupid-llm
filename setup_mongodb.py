"""
MongoDB Setup Script
Initialize only the chat-related collections used by the API.
"""

from mongo_client import chats_collection, db, messages_collection, prompts_collection


def initialize_database():
    """Create the MongoDB collections and indexes used for chat continuity."""
    print("Initializing MongoDB collections...")

    collections = ["messages", "chats", "prompts"]
    for collection_name in collections:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Created collection: {collection_name}")
        else:
            print(f"Collection already exists: {collection_name}")

    print("\nCreating indexes...")
    messages_collection.create_index("chat_id")
    chats_collection.create_index("external_chat_id", unique=True, sparse=True)
    prompts_collection.create_index("project_id")
    print("Indexes created")

    print("\nMongoDB is ready for chat storage.")
    print("Railway SQL should continue to store user/account data.")


if __name__ == "__main__":
    initialize_database()
