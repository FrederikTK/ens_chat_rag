import os
import json
import logging
from tqdm import tqdm
from src.data_processing.embedder import embed_text
from src.rag_system.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def index_processed_files(directory, limit=50):
    vector_store = VectorStore()
    processed_files = [f for f in os.listdir(directory) if f.endswith('.json')][:limit]
    
    for file_name in tqdm(processed_files, desc="Indexing files"):
        file_path = os.path.join(directory, file_name)
        try:
            data = load_json_file(file_path)
            
            text = data['text']
            metadata = data['meta']
            
            embedding = embed_text(text)
            
            vector_store.add_embeddings([embedding], [{
                'id': str(metadata['id']),
                'content': text,
                'url': metadata['url'],
                'title': metadata['title'],
                'time_requested': metadata['time_requested']
            }])
            
            logger.info(f"Indexed file: {file_name}")
        except Exception as e:
            logger.error(f"Error processing file {file_name}: {str(e)}")

    stats = vector_store.get_index_stats()
    logger.info(f"Indexing complete. Total vectors in index: {stats['total_vector_count']}")

if __name__ == "__main__":
    processed_directory = "/app/data/processed/json_files"
    index_processed_files(processed_directory)