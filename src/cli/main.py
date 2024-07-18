# src/cli/main.py
import click
from src.chatbot.agent import ChatbotAgent
from src.data_ingestion.extractor import fetch_data
from src.data_processing.text_splitter import process_directory
from src.rag_system.vector_store import VectorStore
from src.rag_system.retriever import Retriever
from config.config import get_llm_config

@click.group()
def cli():
    pass

@cli.command()
@click.option('--message', prompt='Your message')
def chat(message):
    vector_store = VectorStore()
    retriever = Retriever(vector_store)
    llm_config = get_llm_config("gpt3")  # Or another model as default
    agent = ChatbotAgent(retriever, llm_config)
    response = agent.generate_response(message, [])
    click.echo(f"Bot: {response}")

@cli.command()
def extract():
    urls = fetch_data()
    click.echo(f"Extracted {len(urls)} URLs")

def process():
    documents = []  # Load documents from somewhere
    vector_store = VectorStore(dimension=1536, index_name="ensrag")
    retriever = Retriever(vector_store)
    retriever.add_documents(documents)
    click.echo(f"Processed {len(documents)} document chunks")

if __name__ == '__main__':
    cli()