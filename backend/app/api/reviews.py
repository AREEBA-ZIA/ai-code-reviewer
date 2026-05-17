from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.models import PRReview

router = APIRouter()

@router.get("/reviews")
async def get_reviews(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PRReview).order_by(PRReview.created_at.desc()))
    reviews = result.scalars().all()
    return [
        {
            "id": r.id,
            "repo": r.repo_full_name,
            "pr": r.pr_number,
            "title": r.pr_title,
            "status": r.status,
            "tokens": r.tokens_used,
            "cost": r.cost_usd,
        }
        for r in reviews
    ]