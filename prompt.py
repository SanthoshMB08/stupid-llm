from mongo_client import prompts_collection

def add_prompt(project_id, title, content, gender=None):
    """Add a prompt for a project with optional gender specification"""
    prompt_doc = {
        "project_id": project_id,
        "title": title,
        "content": content,
        "gender": gender  # None, "male", or "female"
    }
    result = prompts_collection.insert_one(prompt_doc)
    return result.inserted_id

def get_prompts(project_id, gender=None):
    """Get prompts for a project, optionally filtered by gender"""
    query = {"project_id": project_id}
    if gender:
        query["gender"] = gender
    
    results = list(prompts_collection.find(query))
    return [(r.get("title"), r.get("content"), r.get("gender")) for r in results]

def get_base_prompt(project_id, gender=None):
    """Get the base system prompt for a gender, falls back to None gender if not found"""
    # First try to find a prompt for the specific gender
    if gender:
        gender_prompt = prompts_collection.find_one({
            "project_id": project_id,
            "gender": gender,
            "title": "base_prompt"
        })
        if gender_prompt:
            return gender_prompt.get("content", "")
    
    # Fall back to generic prompt
    generic_prompt = prompts_collection.find_one({
        "project_id": project_id,
        "gender": None,
        "title": "base_prompt"
    })
    
    return generic_prompt.get("content", "You are a helpful AI assistant.") if generic_prompt else "You are a helpful AI assistant."


def get_gender_base_prompt(gender=None):
    """Return a built-in gender-specific base prompt without requiring a project."""
    prompts = {
        "male": (
            "You are Aiden, a sharp male friend with a casual, bold, street-smart tone. "
            "You can speak with attitude and confidence about international affairs, culture, "
            "politics, sports, and everyday life, but stay useful, clear, and not abusive."
        ),
        "female": (
            "You are Mira, a confident female friend with a warm, expressive, witty tone. "
            "You can talk naturally about international affairs, culture, politics, sports, "
            "and everyday life while staying thoughtful, engaging, and supportive."
        ),
    }
    return prompts.get(gender, "You are Nova, a helpful AI assistant with a natural conversational tone.")
