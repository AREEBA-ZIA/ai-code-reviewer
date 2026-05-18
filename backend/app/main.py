from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.webhook import router as webhook_router
from app.api.reviews import router as reviews_router

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered GitHub PR code reviewer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
allow_origins=[
    "http://localhost:5173", 
    "http://localhost:5174",
    "https://terrific-delight-production-de38.up.railway.app"
],    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router, prefix="/api")
app.include_router(reviews_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Code Reviewer is running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "app": settings.APP_NAME}
