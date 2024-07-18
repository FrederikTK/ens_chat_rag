from fastapi import APIRouter, HTTPException
from src.data_ingestion.extractor import fetch_data
from src.data_ingestion.load_data import scrape_url, scrape_urls
from src.data_ingestion.summarizer import summarize_text
from src.utils.chunker import process_directory
from src.data_processing.embedder import embed_text
from src.api.models.request_models import DocumentRequest, ProcessRequest
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter()

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
        vector_store = VectorStore(dimension=1536, index_name="ensrag")
        retriever = Retriever(vector_store)
        retriever.add_documents(processed_docs)
        return {"status": "success", "processed_count": len(processed_docs)}
    except Exception as e:
        logger.error(f"Error processing documents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")