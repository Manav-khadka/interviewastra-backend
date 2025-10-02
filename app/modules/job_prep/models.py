from sqlalchemy import Column, DateTime, func, String, TEXT, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.db.base import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)  # Assuming companies table exists
    title = Column(String(255), nullable=False)
    description = Column(TEXT, nullable=False)
    job_metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class JobPrepKit(Base):
    __tablename__ = "job_prep_kits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_descriptions.id"), nullable=False)
    title = Column(String(255), nullable=False)
    email_draft = Column(TEXT, nullable=True)
    cover_letter = Column(TEXT, nullable=True)
    hr_questions = Column(JSONB, nullable=True)
    managerial_questions = Column(JSONB, nullable=True)
    technical_questions = Column(JSONB, nullable=True)
    dsa_questions = Column(JSONB, nullable=True)
    puzzles = Column(JSONB, nullable=True)
    meta = Column(JSONB, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())