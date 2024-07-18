import logging
from fastapi import FastAPI
from src.api.routes import chat, data

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI()

# Include routers
app.include_router(chat.router)
app.include_router(data.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown.")

# Add a simple root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Welcome to the Sparenergi RAG System API"}