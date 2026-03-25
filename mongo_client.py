from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://santhoshmb08_db_user:fKpbO9bEPNsSIRVS@stupid-db.awnbrjs.mongodb.net/?appName=stupid-db")
DB_NAME = os.getenv("DB_NAME", "chatbot_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
messages_collection = db["messages"]
chats_collection = db["chats"]
prompts_collection = db["prompts"]

# Create indexes for faster queries
messages_collection.create_index("chat_id")
chats_collection.create_index("external_chat_id", unique=True, sparse=True)
prompts_collection.create_index("project_id")

print(f"Connected to MongoDB: {DB_NAME}")
