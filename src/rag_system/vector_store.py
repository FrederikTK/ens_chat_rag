# src/rag_system/vector_store.py

import os
import numpy as np
from pinecone import Pinecone, ServerlessSpec

class VectorStore:
    def __init__(self, dimension=1536, index_name=os.getenv("PINECONE_NAME")):
        self.dimension = dimension
        self.index_name = index_name
        
        # Initialize Pinecone
        self.pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        # Check if the index exists, if not create it
        if self.index_name not in self.pinecone.list_indexes().names():
            self.pinecone.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        # Connect to the index
        self.index = self.pinecone.Index(self.index_name)

    def add_embeddings(self, embeddings, documents):
        vectors = []
        for i, (embedding, document) in enumerate(zip(embeddings, documents)):
            vector = {
                'id': str(i),
                'values': embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
                'metadata': {'content': document['content'], 'url': document.get('url', '')}
            }
            vectors.append(vector)

        # Upsert vectors in batches (Pinecone has a limit on batch size)
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            self.index.upsert(vectors=vectors[i:i+batch_size])

    def search(self, query_embedding, k=5):
        query_vector = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
        results = self.index.query(vector=query_vector, top_k=k, include_metadata=True)
        
        return [
            {
                'content': match['metadata']['content'],
                'url': match['metadata'].get('url', ''),
                'score': match['score']
            }
            for match in results['matches']
        ]

    def delete_all(self):
        self.index.delete(delete_all=True)