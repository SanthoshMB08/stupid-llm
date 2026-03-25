# MongoDB + LLM API + Gender-Specific Prompts - Migration Guide

## Overview
Your chatbot has been updated to:
- ✅ Use **MongoDB** for data persistence (replacing Supabase)
- ✅ Continue using **Groq LLM API** for intelligent responses
- ✅ Keep **RAG (Retrieval Augmented Generation)** search functionality
- ✅ Support **gender-specific base prompts** (male, female, or generic)

## Key Changes

### 1. Database Migration (Supabase → MongoDB)

#### New File: `mongo_client.py`
- Connects to MongoDB using `pymongo`
- Creates collections: `messages`, `chats`, `projects`, `prompts`, `users`
- Automatically creates indexes for performance

#### Updated Files:
- **database.py**: Now uses MongoDB instead of Supabase
  - `create_project(user_id, name)` - Create projects
  - `get_projects(user_id)` - Retrieve user projects
  - `create_chat(user_id, project_id, gender=None)` - Create chat with gender
  - `get_chat_gender(chat_id)` - Retrieve chat's gender

- **prompt.py**: Enhanced with gender support
  - `add_prompt(project_id, title, content, gender=None)` - Add gender-specific prompts
  - `get_prompts(project_id, gender=None)` - Get prompts by gender
  - `get_base_prompt(project_id, gender=None)` - Get base system prompt with gender fallback

- **chat.py**: Updated to use gender-specific prompts
  - `send_message(chat_id, user_input, project_id)` - Now uses gender-aware prompts
  - Retrieves gender from chat metadata
  - Applies appropriate base prompt based on gender

### 2. Gender-Specific Prompts

Each chat can be created with a gender value:
```python
from database import create_chat
chat_id = create_chat(user_id="user123", project_id="proj456", gender="male")
```

When sending a message, the system will:
1. Look for a prompt for that specific gender
2. Fall back to a generic prompt if gender-specific not found
3. Use "You are a helpful AI assistant." as final fallback

#### Adding Gender-Specific Prompts:
```python
from prompt import add_prompt

# Add male-specific base prompt
add_prompt(project_id="proj456", title="base_prompt", content="You are a helpful assistant specialized for male audiences.", gender="male")

# Add female-specific base prompt
add_prompt(project_id="proj456", title="base_prompt", content="You are a helpful assistant specialized for female audiences.", gender="female")

# Add generic prompt (used if gender not specified or not found)
add_prompt(project_id="proj456", title="base_prompt", content="You are a helpful AI assistant.", gender=None)
```

### 3. RAG (Retrieval Augmented Generation)

✅ **No changes to RAG implementation** - It continues to work the same way!
- Uses TF-IDF vectorizer for similarity matching
- Retrieves top-k relevant messages from chat history
- Passes context to LLM before user query

### 4. LLM API

✅ **No changes** - Still uses **Groq API**
- Model: `openai/gpt-oss-120b`
- Temperature: 0.7
- Ensure `GROQ_API_KEY` is set in `.env`

## Setup Instructions

### Step 1: Install New Dependencies
```bash
pip install pymongo
# Or install all fresh
pip install -r requirements.txt
```

### Step 2: Setup Environment Variables
Create or update `.env` file:
```
MONGO_URI=mongodb://localhost:27017
# For MongoDB Atlas: mongodb+srv://username:password@cluster.mongodb.net/...
DB_NAME=chatbot_db
GROQ_API_KEY=your_groq_api_key
```

### Step 3: Initialize MongoDB
Run the setup script:
```bash
python setup_mongodb.py
```

### Step 4: Create Base Prompts
```python
from prompt import add_prompt

# For your project
project_id = "your_project_id"

add_prompt(project_id, "base_prompt", "Your male-specific prompt here", gender="male")
add_prompt(project_id, "base_prompt", "Your female-specific prompt here", gender="female")
add_prompt(project_id, "base_prompt", "Generic prompt as fallback", gender=None)
```

Leave blank if not specified - the system will use fallback prompts.

## Usage Example

```python
from database import create_project, create_chat
from chat import send_message
from prompt import add_prompt

# 1. Create a project
project_id = create_project("user123", "My Chatbot")

# 2. Add gender-specific prompts
add_prompt(project_id, "base_prompt", "Talk like a mentor for men.", gender="male")
add_prompt(project_id, "base_prompt", "Talk like a mentor for women.", gender="female")

# 3. Create a chat for a male user
chat_id = create_chat("user123", project_id, gender="male")

# 4. Send messages
response = send_message(chat_id, "Hello!", project_id)
# This will use the male-specific base prompt
print(response)

# 5. Create chat for female user
chat_id_f = create_chat("user123", project_id, gender="female")
response_f = send_message(chat_id_f, "Hello!", project_id)
# This will use the female-specific base prompt
print(response_f)
```

## File Structure

```
project/
├── mongo_client.py          # NEW: MongoDB connection
├── setup_mongodb.py         # NEW: Database initialization script
├── .env.example             # NEW: Example environment variables
├── chat.py                  # UPDATED: Gender-aware chat
├── database.py              # UPDATED: MongoDB operations
├── prompt.py                # UPDATED: Gender-specific prompts
├── llm.py                   # UNCHANGED: Groq API
├── rag.py                   # UNCHANGED: RAG search
├── app.py                   # No changes needed
├── requirements.txt         # UPDATED: pymongo instead of supabase
└── ...
```

## Important Notes

- **Prompts can be blank**: Leave `content` empty if you don't want gender-specific customization
- **Gender values**: Use `"male"`, `"female"`, or `None` (for generic)
- **Backwards compatible**: If no gender is specified, system uses generic prompts
- **Indexes automatically created**: MongoDB indexes are created for fast queries
- **RAG unchanged**: Similarity search and context retrieval work exactly as before

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running locally OR MongoDB Atlas connection string is correct
- Check `MONGO_URI` in `.env`

### Missing Prompts
- Run `setup_mongodb.py` to initialize collections
- Add prompts for your project using `add_prompt()`

### LLM API Errors
- Verify `GROQ_API_KEY` is set correctly in `.env`
- Check Groq console for API quota
