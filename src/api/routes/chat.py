# src/api/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException
from src.chatbot.dependencies import get_agent
from src.chatbot.agent import ChatbotAgent
from src.api.models.request_models import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest, agent: ChatbotAgent = Depends(get_agent)):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    response = agent.generate_response(request.message)
    return response

def test_chat():
    print("Testing chat functionality...")
    questions = [
        "Kan du give mig nogle tips til at spare på energien i hjemmet?",
        "Hvad er de mest energieffektive hvidevarer?",
        "Hvordan kan jeg reducere mit CO2-fodaftryk?"
    ]
    for question in questions:
        result = call_endpoint("/chat", "POST", {"message": question})
        print(f"Chat response for '{question}':")
        print(result.get('response', ''))
        print("Sources:")
        for source in result.get('sources', []):
            print(f"- {source}")
        print()