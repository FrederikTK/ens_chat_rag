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
    vector_store = VectorStore(768)  # Assuming 768-dimensional embeddings
    retriever = Retriever(vector_store)
    llm_config = get_llm_config("gpt3")  # Or another model as default
    agent = ChatbotAgent(retriever, llm_config)
    response = agent.generate_response(message, [])
    click.echo(f"Bot: {response}")

@cli.command()
def extract():
    urls = fetch_data()
    click.echo(f"Extracted {len(urls)} URLs")

@cli.command()
def process():
    documents = []  # Load documents from somewhere
    processed = process_directory(documents)
    click.echo(f"Processed {len(processed)} document chunks")

if __name__ == '__main__':
    cli()