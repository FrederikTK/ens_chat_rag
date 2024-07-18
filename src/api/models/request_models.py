# src/api/models/request_models.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class DocumentRequest(BaseModel):
    url: str
    content: str

class ProcessRequest(BaseModel):
    document_ids: list[str]