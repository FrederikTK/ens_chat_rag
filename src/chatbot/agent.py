# src/chatbot/agent.py
from src.rag_system.retriever import Retriever
from src.utils.llm_interface import call_llm_api

class ChatbotAgent:
    def __init__(self, retriever: Retriever, llm_config):
        self.retriever = retriever
        self.llm_config = llm_config

    def generate_response(self, user_input, conversation_history):
        relevant_docs = self.retriever.get_relevant_documents(user_input)
        context = "\n".join(doc['content'] for doc in relevant_docs)
        prompt = f"Context: {context}\n\nConversation History: {conversation_history}\n\nUser: {user_input}\n\nAssistant:"
        response = call_llm_api(self.llm_config, {"content": prompt})
        return response