# The line `from sqlalchemy import Column, DateTime, func, String, ForeignKey, Enum` is importing
# specific elements from the SQLAlchemy library that are commonly used when defining database models
# using SQLAlchemy's Object-Relational Mapping (ORM) framework.
from sqlalchemy import Column, DateTime, func, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
import enum
from app.db.base import Base

class AnalysisType(str, enum.Enum):
    general = "general"
    job_specific = "job_specific"

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_descriptions.id"), nullable=True)
    analysis_type = Column(Enum(AnalysisType), nullable=False)
    feedback_json = Column(JSONB, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())