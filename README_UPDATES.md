# 🤖 MongoDB + LLM API + Gender-Aware Chatbot

Your chatbot has been upgraded from Supabase to MongoDB with gender-specific prompt support!

## ✨ What's New

✅ **MongoDB** - More flexible NoSQL database  
✅ **Gender-Specific Prompts** - Different behaviors for male/female users  
✅ **LLM API** - Groq API (unchanged)  
✅ **RAG Search** - Maintained (TF-IDF based)  

---

## 🎯 Get Started in 3 Steps

### Step 1️⃣: Install & Configure
```bash
# Install new dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env

# Edit .env with your credentials:
# MONGO_URI=mongodb://localhost:27017
# GROQ_API_KEY=your-key-here
```

### Step 2️⃣: Initialize Database
```bash
python setup_mongodb.py
```

### Step 3️⃣: Run Example
```bash
python example_usage.py
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **CHANGES_SUMMARY.md** | Overview of all changes |
| **MIGRATION_GUIDE.md** | Complete setup & usage guide |
| **API_REFERENCE.py** | Quick API reference with examples |
| **example_usage.py** | Working example code |
| **.env.example** | Environment variables template |

---

## 🚀 Quick Usage

```python
from database import create_project, create_chat
from chat import send_message
from prompt import add_prompt

# 1. Create project
proj_id = create_project("user123", "My Bot")

# 2. Add gender-specific prompts
add_prompt(proj_id, "base_prompt", "Male prompt here", gender="male")
add_prompt(proj_id, "base_prompt", "Female prompt here", gender="female")

# 3. Chat as male
male_chat = create_chat("user123", proj_id, gender="male")
print(send_message(male_chat, "Hello!", proj_id))

# 4. Chat as female
female_chat = create_chat("user123", proj_id, gender="female")
print(send_message(female_chat, "Hello!", proj_id))
```

---

## 📁 File Structure

```
chat_bot - Copy/
├── mongo_client.py           ← NEW: MongoDB connection
├── setup_mongodb.py          ← NEW: DB initialization
├── MIGRATION_GUIDE.md        ← NEW: Full guide
├── CHANGES_SUMMARY.md        ← NEW: Change summary
├── API_REFERENCE.py          ← NEW: API reference
├── example_usage.py          ← NEW: Working example
├── .env.example              ← NEW: Environment template
│
├── chat.py                   ← UPDATED: MongoDB + Gender
├── database.py               ← UPDATED: MongoDB + Gender
├── prompt.py                 ← UPDATED: Gender support
├── project.py                ← UPDATED: MongoDB
├── requirements.txt          ← UPDATED: pymongo
│
├── llm.py                    ← UNCHANGED
├── rag.py                    ← UNCHANGED
├── app.py                    ← UNCHANGED
└── ...
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```
MONGO_URI=mongodb://localhost:27017
# For MongoDB Atlas: mongodb+srv://user:pass@cluster.mongodb.net/

DB_NAME=chatbot_db
GROQ_API_KEY=your_groq_api_key_here
```

### Supported Genders
- `"male"` - Use male-specific prompt
- `"female"` - Use female-specific prompt  
- `None` - Use generic/fallback prompt

---

## 🔧 Common Tasks

### Setup Initial Prompts
```python
from prompt import add_prompt

project_id = "your_project_id"

# Male prompt
add_prompt(project_id, "base_prompt", 
    "You are a helpful mentor for men.", gender="male")

# Female prompt
add_prompt(project_id, "base_prompt",
    "You are a helpful mentor for women.", gender="female")

# Fallback
add_prompt(project_id, "base_prompt",
    "You are a helpful AI assistant.", gender=None)
```

### Create Multi-Gender Chats
```python
from database import create_chat

for gender in ["male", "female", None]:
    chat_id = create_chat("user123", project_id, gender=gender)
    print(f"Created chat for {gender}: {chat_id}")
```

### Send Messages with Gender Context
```python
from chat import send_message

response = send_message(
    chat_id="chat_id_here",
    user_input="Your question",
    project_id="project_id_here"  # Needed for gender-specific prompts
)
```

---

## 🐛 Troubleshooting

**MongoDB Connection Error**
- Ensure MongoDB is running: `mongod`
- Or use MongoDB Atlas connection string in `.env`
- Check `MONGO_URI` format

**LLM API Error**  
- Verify `GROQ_API_KEY` is set in `.env`
- Check API quota at https://console.groq.com/

**No Prompts Found**
- Run `python setup_mongodb.py` first
- Add prompts: `add_prompt(project_id, "base_prompt", "content", gender="male")`

---

## 📖 Learn More

1. **Quick Start**: See `MIGRATION_GUIDE.md`
2. **Full Examples**: See `example_usage.py`
3. **API Docs**: See `API_REFERENCE.py`
4. **Changes**: See `CHANGES_SUMMARY.md`

---

## ✅ Next Steps

1. ✓ Install dependencies: `pip install -r requirements.txt`
2. ✓ Setup MongoDB and environment variables
3. ✓ Run initialization: `python setup_mongodb.py`
4. ✓ Try example: `python example_usage.py`
5. ✓ Customize prompts for your use case
6. ✓ Integrate into your app!

---

**Questions?** Check the docs or look at working examples in `example_usage.py` 🚀
