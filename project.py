from mongo_client import projects_collection

def create_project(user_id, name, description=""):
    """Create a new project with optional description"""
    result = projects_collection.insert_one({
        "user_id": user_id,
        "name": name,
        "description": description
    })
    return str(result.inserted_id)

def get_projects(user_id):
    """Get all projects for a user, ordered by creation (newest first)"""
    results = list(projects_collection.find({"user_id": user_id}).sort("_id", -1))
    return [(str(r["_id"]), r["name"]) for r in results]