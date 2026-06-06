from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime

from backend.models.database import Base


class Documentation(Base):
    __tablename__ = "documentations"

    id = Column(String, primary_key=True)
    code_id = Column(String, nullable=False)
    doc_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
