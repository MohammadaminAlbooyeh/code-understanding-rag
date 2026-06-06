from sqlalchemy import Column, String, Text, DateTime, Integer
from datetime import datetime, timezone

from backend.models.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(String, primary_key=True)
    code_id = Column(String, nullable=False)
    chunk_index = Column(Integer, default=0)
    chunk_text = Column(Text, nullable=False)
    vector_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=_utcnow)
