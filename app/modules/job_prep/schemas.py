from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class JobDescriptionBase(BaseModel):
    title: str
    description: str
    metadata: Optional[Dict[str, Any]] = None

class JobDescriptionCreate(JobDescriptionBase):
    pass

class JobDescriptionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class JobDescription(JobDescriptionBase):
    id: uuid.UUID
    user_id: uuid.UUID
    company_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JobPrepKitBase(BaseModel):
    title: str
    email_draft: Optional[str] = None
    cover_letter: Optional[str] = None
    hr_questions: Optional[Dict[str, Any]] = None
    managerial_questions: Optional[Dict[str, Any]] = None
    technical_questions: Optional[Dict[str, Any]] = None
    dsa_questions: Optional[Dict[str, Any]] = None
    puzzles: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None

class JobPrepKitCreate(JobPrepKitBase):
    resume_id: uuid.UUID
    job_id: uuid.UUID

class JobPrepKitUpdate(BaseModel):
    title: Optional[str] = None
    email_draft: Optional[str] = None
    cover_letter: Optional[str] = None
    hr_questions: Optional[Dict[str, Any]] = None
    managerial_questions: Optional[Dict[str, Any]] = None
    technical_questions: Optional[Dict[str, Any]] = None
    dsa_questions: Optional[Dict[str, Any]] = None
    puzzles: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None

class JobPrepKitResponse(JobPrepKitBase):
    id: uuid.UUID
    user_id: uuid.UUID
    resume_id: uuid.UUID
    job_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True