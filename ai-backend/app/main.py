from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.chat import router as chat_router


from app.core.config import settings

app = FastAPI(
    title="AI Backend",
    version="1.0.0",
)

allowed_origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
] if settings.cors_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/")
def root():
    return {
        "message": "AI Backend API is running",
        "health": "/health",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok"}