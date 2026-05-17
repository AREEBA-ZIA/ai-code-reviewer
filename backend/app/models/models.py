from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    github_repo_id = Column(Integer, unique=True)
    full_name = Column(String, unique=True)  # e.g. "user/repo"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class PRReview(Base):
    __tablename__ = "pr_reviews"

    id = Column(Integer, primary_key=True, index=True)
    repo_full_name = Column(String)
    pr_number = Column(Integer)
    pr_title = Column(String)
    status = Column(String, default="pending")   # pending / done / failed
    review_output = Column(Text)                 # AI response JSON
    tokens_used = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())