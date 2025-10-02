from sqlalchemy import Column, String, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base
import enum

class AuthProviderEnum(str, enum.Enum):
    email = "email"  # Changed from 'local' to match database
    google = "google"
    github = "github"

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)  # Nullable for OAuth
    auth_provider = Column(Enum(AuthProviderEnum), default=AuthProviderEnum.email)
    provider_id = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.user)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())