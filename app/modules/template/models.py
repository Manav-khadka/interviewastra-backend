from sqlalchemy import Column, Integer, String, TEXT, DateTime, func, Enum
from app.db.base import Base
import enum

class TemplateEngineEnum(str, enum.Enum):
    latex = "latex"

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    engine = Column(Enum(TemplateEngineEnum), default=TemplateEngineEnum.latex)
    content = Column(TEXT, nullable=False)
    preview_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())