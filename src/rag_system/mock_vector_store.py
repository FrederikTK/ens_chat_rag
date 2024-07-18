# src/rag_system/mock_vector_store.py
import numpy as np

class MockVectorStore:
    def __init__(self, dimension, index_name):
        self.dimension = dimension
        self.index_name = index_name
        self.documents = []
        self.embeddings = []

    def add_embeddings(self, embeddings, documents):
        self.embeddings.extend(embeddings)
        self.documents.extend(documents)

    def search(self, query_embedding, k=5):
        # For simplicity, just return the first k documents
        return self.documents[:k]
