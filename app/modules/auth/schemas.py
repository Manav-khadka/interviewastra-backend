from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class UserBase(BaseModel):
    username: str
    name: str
    email: EmailStr
    role: str = "user"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"

class OAuthUserCreate(BaseModel):
    """Schema for OAuth login (Google, GitHub)"""
    email: EmailStr
    name: str
    provider_id: str
    username: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: uuid.UUID
    auth_provider: str
    provider_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    """Response model for login endpoints"""
    access_token: str
    token_type: str
    user: dict