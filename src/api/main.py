import logging
from fastapi import FastAPI
from src.api.routes import chat, data

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
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
