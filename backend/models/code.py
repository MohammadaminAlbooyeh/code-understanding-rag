from sqlalchemy import Column, String, Text, DateTime, Integer
from datetime import datetime, timezone

from backend.models.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Code(Base):
    __tablename__ = "codes"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    language = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    size = Column(Integer, default=0)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
