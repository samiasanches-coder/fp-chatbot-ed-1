from fastapi import FastAPI
from pydantic import BaseModel

from app.chatbot import Chatbot

app = FastAPI(title="FP Gemini Edition 1 API")
chatbot = Chatbot()


class ChatRequest(BaseModel):
    session_id: str = "default"
    message: str


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "fp-gemini-edition-1"}


@app.post("/chat")
def chat(request: ChatRequest):
    response = chatbot.respond(request.message, session_id=request.session_id)
    return {"session_id": request.session_id, "response": response, "status": "ok"}


@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    session = chatbot.session_manager.load_session(session_id)
    return session.to_dict()
