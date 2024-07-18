from src.rag_system.vector_store import VectorStore
from src.data_processing.embedder import embed_text

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def get_relevant_documents(self, query, k=5):
        query_embedding = embed_text(query)
        return self.vector_store.search(query_embedding, k)

    def add_documents(self, documents):
        embeddings = [embed_text(doc['content']) for doc in documents]
        self.vector_store.add_embeddings(embeddings, documents)