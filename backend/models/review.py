from sqlalchemy import Column, String, Text, DateTime, Float, JSON
from datetime import datetime

from backend.models.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True)
    code_id = Column(String, nullable=False)
    quality_score = Column(Float, default=0.0)
    issues = Column(JSON, default=list)
    suggestions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
