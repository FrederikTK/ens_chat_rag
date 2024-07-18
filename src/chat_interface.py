import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.chatbot.agent import ChatbotAgent
from src.rag_system.vector_store import VectorStore
from src.rag_system.retriever import Retriever
from config.config import get_llm_config

def initialize_agent():
    vector_store = VectorStore()
    retriever = Retriever(vector_store)
    llm_config = get_llm_config("gpt3")  # You can change this to use a different model if needed
    return ChatbotAgent(retriever, llm_config)

def chat_loop(agent):
    print("Welcome to the Sparenergi RAG Chat System!")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Thank you for using the Sparenergi RAG Chat System. Goodbye!")
            break

        response = agent.generate_response(user_input)
        
        print("\nAssistant: ", response['response'])
        
        print("\nRelevant Documents:")
        for i, doc in enumerate(response['sources'], 1):
            print(f"{i}. URL: {doc['url']}")
            print(f"   Score: {doc['score']:.4f}")
            print(f"   Content snippet: {doc['title'][:100]}...")
            print()

        print("--------------------\n")

if __name__ == "__main__":
    agent = initialize_agent()
    chat_loop(agent)