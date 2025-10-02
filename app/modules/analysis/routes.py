import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.resumes.models import Resume
from app.modules.job_prep.models import JobDescription
from app.modules.analysis.models import ResumeAnalysis
from app.modules.analysis.schemas import ResumeAnalysisCreate, ResumeAnalysisResponse
from app.core.dependencies import get_current_user
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/", response_model=ResumeAnalysisResponse)
async def create_analysis(analysis: ResumeAnalysisCreate, resume_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    job_desc = None
    if analysis.job_id:
        job = db.query(JobDescription).filter(JobDescription.id == analysis.job_id, JobDescription.user_id == current_user.id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job description not found")
        job_desc = job.description
    
    feedback = await AIService.analyze_resume(resume.content_json, job_desc)
    
    db_analysis = ResumeAnalysis(
        resume_id=resume_id,
        job_id=analysis.job_id,
        analysis_type=analysis.analysis_type,
        feedback_json=feedback
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

@router.get("/", response_model=list[ResumeAnalysisResponse])
def get_analyses(resume_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db.query(ResumeAnalysis).filter(ResumeAnalysis.resume_id == resume_id).all()