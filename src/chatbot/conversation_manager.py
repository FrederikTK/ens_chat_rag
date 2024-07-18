# src/chatbot/conversation_manager.py
from src.chatbot.agent import ChatbotAgent

class ConversationManager:
    def __init__(self, agent: ChatbotAgent):
        self.agent = agent
        self.conversation_history = []

    def add_message(self, role, content):
        self.conversation_history.append({"role": role, "content": content})

    def get_response(self, user_input):
        self.add_message("user", user_input)
        response = self.agent.generate_response(user_input)
        self.add_message("assistant", response["response"])
        return response["response"]

    def clear_history(self):
        self.conversation_history = []
