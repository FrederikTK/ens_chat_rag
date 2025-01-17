from fastapi import APIRouter, HTTPException
from src.data_ingestion.extractor import fetch_data
from src.data_ingestion.load_data import scrape_url
from src.data_ingestion.summarizer import summarize_text
from src.utils.chunker import process_directory
from src.data_processing.embedder import embed_text
from src.api.models.request_models import DocumentRequest, ProcessRequest
from src.rag_system.vector_store import VectorStore
from src.rag_system.retriever import Retriever
import logging
import uuid
logger = logging.getLogger("uvicorn.error")

router = APIRouter()

vector_store = VectorStore()
retriever = Retriever(vector_store)

@router.post("/process-and-index")
async def process_and_index_endpoint(request: DocumentRequest):
    try:
        # Generate embedding
        embedding = embed_text(request.content)
        
        # Create a unique ID for this document
        doc_id = str(uuid.uuid4())
        
        # Add to vector store
        vector_store.add_embeddings([embedding], [{
            'id': doc_id,
            'content': request.content,
            'url': request.url
        }])
        
        logger.info(f"Indexed document: {doc_id}, URL: {request.url}")
        
        return {"success": True, "message": "Document processed and indexed successfully", "id": doc_id}
    except Exception as e:
        logger.error(f"Error in process_and_index: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embed")
async def embed_endpoint(request: dict):
    try:
        embedding = embed_text(request["text"])
        return {"embedding": embedding.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_endpoint(request: dict):
    try:
        query_embedding = embed_text(request["query"])
        results = vector_store.search(query_embedding)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-urls")
async def extract_urls_endpoint():
    try:
        urls = fetch_data(1, 1000)
        return {"urls": urls}
    except Exception as e:
        logger.error(f"Error extracting URLs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/scrape")
async def scrape_url_endpoint(request: DocumentRequest):
    try:
        scraped_data = scrape_url(request.url)
        return {"scraped_data": scraped_data}
    except Exception as e:
        logger.error(f"Error scraping URL: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/summarize")
async def summarize_endpoint(request: DocumentRequest):
    try:
        summary = summarize_text(request.content)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error summarizing content: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/process")
async def process_documents_endpoint(request: ProcessRequest):
    try:
        processed_docs = process_directory(request.document_ids)
        retriever = Retriever(vector_store)
        retriever.add_documents(processed_docs)
        return {"status": "success", "processed_count": len(processed_docs)}
    except Exception as e:
        logger.error(f"Error processing documents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")