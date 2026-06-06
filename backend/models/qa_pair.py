from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime

from backend.models.database import Base


class QAPair(Base):
    __tablename__ = "qa_pairs"

    id = Column(String, primary_key=True)
    code_id = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
