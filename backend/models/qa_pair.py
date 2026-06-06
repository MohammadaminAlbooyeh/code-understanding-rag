from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime, timezone

from backend.models.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class QAPair(Base):
    __tablename__ = "qa_pairs"

    id = Column(String, primary_key=True)
    code_id = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(Text, default="")
    created_at = Column(DateTime, default=_utcnow)
