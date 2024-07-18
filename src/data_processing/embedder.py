# embedder.py

import os
import json
import numpy as np
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

def embed_text(text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        model=model,
        input=text
    )
    embedding = response.data[0].embedding
    return np.array(embedding)

def embed_files(directory, model="text-embedding-3-small"):
    embeddings = []
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                embedding = embed_text(data["text"], model)
                data["embedding"] = embedding.tolist()
                embeddings.append(data)
    
    return embeddings

def save_embeddings(embeddings, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for i, embedding in enumerate(embeddings):
        output_path = os.path.join(output_dir, f"embedded_{i}.json")
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(embedding, file, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Embed text chunks and save embeddings.")
    parser.add_argument('--chunk_dir', required=True, help='Directory where chunked files are located')
    parser.add_argument('--embed_dir', required=True, help='Directory to save embeddings')
    parser.add_argument('--model', default='text-embedding-3-small', help='Embedding model to use')
    args = parser.parse_args()

    embeddings = embed_files(args.chunk_dir, args.model)
    save_embeddings(embeddings, args.embed_dir)
    print(f"Generated and saved {len(embeddings)} embeddings.")

if __name__ == "__main__":
    main()