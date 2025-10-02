from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class ResumeAnalysisBase(BaseModel):
    analysis_type: str
    feedback_json: Dict[str, Any]

class ResumeAnalysisCreate(ResumeAnalysisBase):
    job_id: Optional[uuid.UUID] = None

class ResumeAnalysisUpdate(BaseModel):
    feedback_json: Optional[Dict[str, Any]] = None

class ResumeAnalysisResponse(ResumeAnalysisBase):
    id: uuid.UUID
    resume_id: uuid.UUID
    job_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True