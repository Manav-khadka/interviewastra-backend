from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.resumes.models import Resume
from app.modules.job_prep.models import JobDescription, JobPrepKit
from app.modules.job_prep.schemas import JobPrepKitCreate, JobPrepKitResponse
from app.core.dependencies import get_current_user
from app.services.ai_service import AIService
import uuid

router = APIRouter()

@router.post("/", response_model=JobPrepKitResponse)
async def create_prep_kit(kit: JobPrepKitCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == kit.resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    job = db.query(JobDescription).filter(JobDescription.id == kit.job_id, JobDescription.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Assume experience is in resume or user profile, for now placeholder
    experience = "Based on resume content"  # TODO: extract from resume
    
    kit_data = await AIService.generate_prep_kit(resume.content_json, job.description, experience)
    
    db_kit = JobPrepKit(**kit.dict(), user_id=current_user.id, **kit_data)
    db.add(db_kit)
    db.commit()
    db.refresh(db_kit)
    return db_kit

@router.get("/", response_model=list[JobPrepKitResponse])
def get_prep_kits(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(JobPrepKit).filter(JobPrepKit.user_id == current_user.id).all()

@router.get("/{kit_id}", response_model=JobPrepKitResponse)
def get_prep_kit(kit_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    kit = db.query(JobPrepKit).filter(JobPrepKit.id == kit_id, JobPrepKit.user_id == current_user.id).first()
    if not kit:
        raise HTTPException(status_code=404, detail="Prep kit not found")
    return kit