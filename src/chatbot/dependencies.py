# src/chatbot/dependencies.py
import os
from src.rag_system.retriever import Retriever
from src.rag_system.mock_vector_store import MockVectorStore  # Use mock vector store for testing
from src.chatbot.agent import ChatbotAgent
from config.config import get_llm_config

def get_agent():
    if os.getenv("USE_MOCK_VECTOR_STORE", "false").lower() == "true":
        vector_store = MockVectorStore(dimension=1536, index_name="mock_index")
    else:
        from src.rag_system.vector_store import VectorStore
        vector_store = VectorStore()  # Ensure you have created this index in Pinecone

    retriever = Retriever(vector_store)
    llm_config = get_llm_config("gpt3")  # Or another model as default
    agent = ChatbotAgent(retriever, llm_config)
    return agent