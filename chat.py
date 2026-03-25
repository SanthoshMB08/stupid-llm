from mongo_client import messages_collection
from llm import chat_completion
from rag import get_relevant_context
from prompt import get_gender_base_prompt
from database import normalize_gender, upsert_chat


PERSONA_NAMES = {
    "male": "Aiden",
    "female": "Mira",
}


def get_messages(chat_id):
    """Retrieve all messages for a chat."""
    try:
        results = list(messages_collection.find({"chat_id": chat_id}).sort("_id", 1))
        return [(row["role"], row["content"]) for row in results]
    except Exception:
        return []


def build_persona_prompt(gender=None):
    """Create the base prompt using gender first."""
    normalized_gender = normalize_gender(gender)
    return get_gender_base_prompt(normalized_gender)


def _format_history_for_rag(history):
    return [f"{role}: {content}" for role, content in history if content]


def send_message(chat_id, user_input, gender):
    """Generate a response using gender prompt + chat history RAG, then save both turns."""
    normalized_gender = normalize_gender(gender)
    chat = upsert_chat(chat_id, gender=normalized_gender)
    active_gender = chat.get("gender")

    history = get_messages(chat_id)
    history_for_rag = _format_history_for_rag(history)
    context = get_relevant_context(history_for_rag, user_input, k=3)

    messages = [{"role": "system", "content": build_persona_prompt(active_gender)}]

    if context:
        context_block = "\n".join(f"- {item}" for item in context)
        messages.append(
            {
                "role": "system",
                "content": f"Use this past chat context for continuity when relevant:\n{context_block}",
            }
        )

    for role, content in history[-8:]:
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})
    reply = chat_completion(messages)

    messages_collection.insert_one(
        {
            "chat_id": chat_id,
            "role": "user",
            "content": user_input,
        }
    )
    messages_collection.insert_one(
        {
            "chat_id": chat_id,
            "role": "assistant",
            "content": reply,
        }
    )

    return {
        "chat_id": chat_id,
        "gender": active_gender,
        "assistant_name": PERSONA_NAMES.get(active_gender, "Nova"),
        "reply": reply,
        "context_used": context,
    }
