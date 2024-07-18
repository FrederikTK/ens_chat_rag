# src/api/routes/chat.py
from fastapi import APIRouter, Depends
from src.chatbot.dependencies import get_agent
from src.chatbot.agent import ChatbotAgent
from src.api.models.request_models import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest, agent: ChatbotAgent = Depends(get_agent)):
    response = agent.generate_response(request.message, [])
    return {"response": response}
