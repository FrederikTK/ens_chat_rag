# src/chatbot/agent.py
from src.rag_system.retriever import Retriever
from src.utils.llm_interface import call_llm_api

class ChatbotAgent:
    """
This module defines the ChatbotAgent class, which is responsible for
generating responses to user inputs by retrieving relevant documents and
using a language model to generate a contextually appropriate response.

Classes:
    ChatbotAgent: A class that interfaces with a retriever and an LLM to
    generate responses.
"""
    def __init__(self, retriever: Retriever, llm_config):
        self.retriever = retriever
        self.llm_config = llm_config

    def generate_response(self, user_input):
        relevant_docs = self.retriever.get_relevant_documents(user_input)
        context = "\n".join([f"Content: {doc['content']}\nSource: {doc['url']}" for doc in relevant_docs])
        prompt = f"Context:\n{context}\n\nUser: {user_input}\n\nAssistant: Provide a response based on the given context. Include [Source: URL] at the end of each piece of information you use."
        response = call_llm_api(self.llm_config, {"content": prompt})
        return {
            "response": response, 
            "sources": relevant_docs
        }