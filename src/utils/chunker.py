import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
from utils.gen_uuid import generate_unique_id
from utils.num_tokens import num_tokens_from_string
from typing import List

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=100
)

def split_document_with_metadata(text_content, metadata):
    splits = text_splitter.split_text(text_content)
    splits_with_metadata = [{"text": split, "meta": metadata} for split in splits]
    return splits_with_metadata

def process_json_file(file_path, id_log_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if "text" not in data or "meta" not in data:
        raise ValueError("Incorrect JSON format")

    text_content = data["text"]
    metadata = {
        "id": data["meta"]["document_id"],
        "url/page": data["meta"]["url"],
        "num_tokens": data["meta"]["num_tokens"],
        "time_requested": data["meta"]["time_requested"],
        "title": data["meta"]["title"]
    }

    return split_document_with_metadata(text_content, metadata)

def process_pdf_file(file_path, id_log_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load_and_split()
    document_id = generate_unique_id(id_log_path)
    results = []

    docs_text = [doc.page_content for doc in documents]

    for i, text in enumerate(docs_text):
        metadata = {
            "id": document_id,
            "url/page": i + 1,
            "num_tokens": num_tokens_from_string(text),
            "time_requested": datetime.now().isoformat(),
            "title": file_path.rsplit("/", 1)[-1],
        }
        results.extend(split_document_with_metadata(text, metadata))

    return results

def process_file(file_path, log_file, id_log_path=None):
    if file_path.endswith('.json'):
        return process_json_file(file_path, id_log_path)
    elif file_path.endswith('.pdf'):
        return process_pdf_file(file_path, id_log_path)
    else:
        raise ValueError("Unsupported file type")

def process_directory(directory: str, log_file: str) -> List[dict]:
    processed_docs = []
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            processed_docs.extend(process_file(file_path, log_file))
    with open(log_file, 'w') as log:
        for doc in processed_docs:
            log.write(f"Processed {doc['meta']['title']}\n")
    return processed_docs

def save_splits_with_metadata(splits, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    for filename, split_contents in splits.items():
        for i, split_content in enumerate(split_contents):
            output_filename = f"{filename.split('.')[0]}_{i}.json"
            output_path = os.path.join(output_directory, output_filename)
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(split_content, file, ensure_ascii=False, indent=4)
