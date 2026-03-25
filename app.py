from typing import List, Literal, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from chat import get_messages, send_message


class ChatRequest(BaseModel):
    chat_id: str = Field(..., min_length=1)
    gender: Literal["male", "female"]
    prompt: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    chat_id: str
    gender: Optional[str]
    assistant_name: str
    reply: str
    context_used: List[str]


app = FastAPI(
    title="Chat API",
    description="FastAPI chatbot with gender-based prompt selection and chat-history RAG.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    try:
        return ChatResponse(
            **send_message(
                chat_id=payload.chat_id,
                user_input=payload.prompt,
                gender=payload.gender,
            )
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/chat/{chat_id}/messages")
def chat_messages(chat_id: str):
    return {
        "chat_id": chat_id,
        "messages": [
            {"role": role, "content": content}
            for role, content in get_messages(chat_id)
        ],
    }


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
