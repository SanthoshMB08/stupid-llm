"""
Quick Start Example - Gender-Aware Chatbot with MongoDB
Demonstrates how to use the updated chatbot system
"""

from database import create_project, create_chat, get_projects
from chat import send_message
from prompt import add_prompt, get_base_prompt
import os

def main():
    # Step 1: Create a project
    print("📁 Creating project...")
    user_id = "user_demo_001"
    project_name = "Gender-Aware Demo"
    
    project_id = create_project(user_id, project_name)
    print(f"✓ Project created: {project_id}\n")
    
    # Step 2: Setup gender-specific prompts
    print("🎯 Setting up gender-specific prompts...\n")
    
    # Male prompt
    male_prompt = """You are a helpful AI mentor specifically trained to assist men. 
You understand male perspectives, challenges, and interests. Be supportive, direct, and practical."""
    add_prompt(project_id, "base_prompt", male_prompt, gender="male")
    print("✓ Male prompt added")
    
    # Female prompt
    female_prompt = """You are a helpful AI mentor specifically trained to assist women.
You understand female perspectives, challenges, and interests. Be supportive, empathetic, and practical."""
    add_prompt(project_id, "base_prompt", female_prompt, gender="female")
    print("✓ Female prompt added")
    
    # Generic prompt (fallback)
    generic_prompt = "You are a helpful, friendly AI assistant for everyone."
    add_prompt(project_id, "base_prompt", generic_prompt, gender=None)
    print("✓ Generic prompt added (fallback)\n")
    
    # Step 3: Create chats for different genders
    print("💬 Creating chat sessions...\n")
    
    # Male user chat
    male_chat_id = create_chat(user_id, project_id, gender="male")
    print(f"✓ Male chat created: {male_chat_id}")
    
    # Female user chat
    female_chat_id = create_chat(user_id, project_id, gender="female")
    print(f"✓ Female chat created: {female_chat_id}")
    
    # Generic user chat
    generic_chat_id = create_chat(user_id, project_id, gender=None)
    print(f"✓ Generic chat created: {generic_chat_id}\n")
    
    # Step 4: Send messages with different genders
    print("🚀 Testing gender-specific responses...\n")
    print("=" * 60)
    
    try:
        # Male chat
        print("👨 MALE USER:")
        print("-" * 60)
        male_response = send_message(male_chat_id, "Hello! Can you help me today?", project_id)
        print(f"Bot: {male_response}\n")
        
        # Female chat
        print("👩 FEMALE USER:")
        print("-" * 60)
        female_response = send_message(female_chat_id, "Hello! Can you help me today?", project_id)
        print(f"Bot: {female_response}\n")
        
        # Generic chat
        print("👤 GENERIC USER:")
        print("-" * 60)
        generic_response = send_message(generic_chat_id, "Hello! Can you help me today?", project_id)
        print(f"Bot: {generic_response}\n")
        
    except Exception as e:
        print(f"⚠️  Error during chat: {e}")
        print("Make sure:")
        print("  1. MongoDB is running (mongodb://localhost:27017)")
        print("  2. GROQ_API_KEY is set in .env")
        print("  3. Dependencies are installed (pip install -r requirements.txt)")
    
    print("=" * 60)
    print("✅ Demo complete!\n")
    
    # Show projects
    print("📊 Projects for user:")
    projects = get_projects(user_id)
    for proj_id, proj_name in projects:
        print(f"  - {proj_name} ({proj_id})")

if __name__ == "__main__":
    print("🚀 Gender-Aware Chatbot Demo\n")
    main()
