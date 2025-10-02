from sqlalchemy import Column, DateTime, func, Boolean, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.db.base import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content_json = Column(JSONB, nullable=False)
    ai_enhanced = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())