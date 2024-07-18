# src/rag_system/vector_store.py
import os
import numpy as np
from pinecone import Pinecone, ServerlessSpec
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.dimension = 1536
        self.index_name = "ensrag"
        
        # Initialize Pinecone
        self.pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        # Check if the index exists, if not create it
        if self.index_name not in self.pinecone.list_indexes().names():
            self.pinecone.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region=os.getenv("PINECONE_ENVIRONMENT")
                )
            )

        # Connect to the index
        self.index = self.pinecone.Index(self.index_name)

    def add_embeddings(self, embeddings, documents):
        vectors = []
        for embedding, doc in zip(embeddings, documents):
            vector = {
                'id': doc['id'],
                'values': embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
                'metadata': {'content': doc['content'], 'url': doc['url']}
            }
            vectors.append(vector)

        # Upsert vectors in batches
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.upsert(vectors=batch)
            logger.info(f"Upserted batch of {len(batch)} vectors to Pinecone")

    def search(self, query_embedding, k=5):
        query_vector = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
        results = self.index.query(vector=query_vector, top_k=k, include_metadata=True)
        
        return [
            {
                'content': match['metadata']['content'],
                'url': match['metadata']['url'],
                'score': match['score']
            }
            for match in results['matches']
        ]

    def delete_all(self):
        self.index.delete(delete_all=True)