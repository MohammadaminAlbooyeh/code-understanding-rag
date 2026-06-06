from sqlalchemy import Column, String, Text, DateTime, JSON
from datetime import datetime

from backend.models.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True)
    code_id = Column(String, nullable=False)
    analysis_type = Column(String, nullable=False)
    results = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
