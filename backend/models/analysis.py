from sqlalchemy import Column, String, Text, DateTime, JSON
from datetime import datetime, timezone

from backend.models.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True)
    code_id = Column(String, nullable=False)
    analysis_type = Column(String, nullable=False)
    results = Column(JSON, default=dict)
    created_at = Column(DateTime, default=_utcnow)
