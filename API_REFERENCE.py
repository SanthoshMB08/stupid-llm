"""
API Quick Reference - Gender-Aware MongoDB Chatbot
"""

# ============================================
# DATABASE OPERATIONS
# ============================================

from database import create_project, create_chat, get_projects, get_chat_gender

# Create a project
project_id = create_project(
    user_id="user123",
    name="My Chatbot"
)

# Get all projects for a user
projects = get_projects(user_id="user123")
# Returns: [("proj_id_1", "My Chatbot"), ("proj_id_2", "Other Bot")]

# Create a chat (with gender)
chat_id = create_chat(
    user_id="user123",
    project_id="proj456",
    gender="male"  # Options: "male", "female", or None
)

# Get chat's gender
gender = get_chat_gender(chat_id)
# Returns: "male", "female", or None


# ============================================
# CHAT & MESSAGING
# ============================================

from chat import send_message, get_messages

# Send a message (uses gender-specific prompt)
response = send_message(
    chat_id="chat789",
    user_input="Hello!",
    project_id="proj456"  # Needed to fetch gender-specific prompt
)

# Get all messages in a chat
messages = get_messages(chat_id="chat789")
# Returns: [("user", "Hello!"), ("assistant", "Hi there!"), ...]


# ============================================
# PROMPT MANAGEMENT
# ============================================

from prompt import add_prompt, get_prompts, get_base_prompt

# Add a gender-specific prompt
add_prompt(
    project_id="proj456",
    title="base_prompt",
    content="You are a helpful mentor for men.",
    gender="male"
)

# Add a generic prompt (fallback)
add_prompt(
    project_id="proj456",
    title="base_prompt",
    content="You are a helpful AI assistant.",
    gender=None
)

# Get all prompts for a project (optionally filtered by gender)
all_prompts = get_prompts(project_id="proj456")
male_prompts = get_prompts(project_id="proj456", gender="male")

# Get the base prompt (with gender fallback logic)
prompt = get_base_prompt(
    project_id="proj456",
    gender="male"
)
# Returns: Male prompt if found, else generic, else default


# ============================================
# LLM API (No Changes)
# ============================================

from llm import chat_completion

# Direct LLM call (if needed)
messages = [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello!"}
]
response = chat_completion(messages)


# ============================================
# RAG SEARCH (No Changes)
# ============================================

from rag import get_relevant_context

# Get relevant context from history
history = ["message 1", "message 2", "message 3"]
context = get_relevant_context(history, "new query", k=3)
# Returns: [relevant_msg_1, relevant_msg_2, ...]


# ============================================
# COMPLETE WORKFLOW EXAMPLE
# ============================================

def setup_chatbot_for_user(user_id, project_name, male_prompt, female_prompt):
    """Setup a complete gender-aware chatbot"""
    
    # 1. Create project
    project_id = create_project(user_id, project_name)
    
    # 2. Add gender-specific prompts
    add_prompt(project_id, "base_prompt", male_prompt, gender="male")
    add_prompt(project_id, "base_prompt", female_prompt, gender="female")
    add_prompt(project_id, "base_prompt", "Generic AI assistant.", gender=None)
    
    return project_id


def chat_with_gender(user_id, project_id, gender, user_message):
    """Send a message in a gender-aware conversation"""
    
    # 1. Create or get chat
    chat_id = create_chat(user_id, project_id, gender)
    
    # 2. Send message (automatically uses gender-specific prompt)
    response = send_message(chat_id, user_message, project_id)
    
    return response


# ============================================
# GENDER VALUES
# ============================================

GENDERS = {
    "male": "Male-specific behavior and prompts",
    "female": "Female-specific behavior and prompts",
    None: "Generic/Fallback behavior"
}

# ============================================
# COMMON OPERATIONS
# ============================================

# Multi-gender chat for same user
def multi_gender_demo(user_id, project_id):
    for gender in ["male", "female", None]:
        chat_id = create_chat(user_id, project_id, gender)
        response = send_message(chat_id, "Hello!", project_id)
        print(f"{gender or 'Generic'}: {response}")

# Add custom prompts for specific use case
def add_therapist_prompts(project_id):
    add_prompt(project_id, "base_prompt", 
        "You are a supportive therapist for men. Focus on practical solutions.",
        gender="male")
    add_prompt(project_id, "base_prompt",
        "You are a supportive therapist for women. Focus on empathy and solutions.",
        gender="female")

# ============================================
# ERROR HANDLING
# ============================================

try:
    chat_id = create_chat(user_id, project_id, gender="male")
    response = send_message(chat_id, "Hello!", project_id)
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Database or LLM error: {e}")
