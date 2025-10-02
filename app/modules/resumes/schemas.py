from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class ResumeBase(BaseModel):
    title: str
    content_json: Dict[str, Any]
    ai_enhanced: bool = False

class ResumeCreate(ResumeBase):
    template_id: int

class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    ai_enhanced: Optional[bool] = None

class ResumeResponse(ResumeBase):
    id: uuid.UUID
    user_id: uuid.UUID
    template_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True