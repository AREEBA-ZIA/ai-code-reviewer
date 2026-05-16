from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.webhook import router as webhook_router

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered GitHub PR code reviewer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Code Reviewer is running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "app": settings.APP_NAME}