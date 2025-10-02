from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modules.resumes.models import Resume
from app.modules.template.models import Template
from app.modules.resumes.schemas import ResumeCreate, ResumeUpdate, ResumeResponse
from app.core.dependencies import get_current_user
from app.services.ai_service import AIService
from app.services.latex_service import LaTeXService
import uuid

router = APIRouter()

@router.post("/", response_model=ResumeResponse)
async def create_resume(resume: ResumeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Check if template exists
    template = db.query(Template).filter(Template.id == resume.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Enhance with AI if requested
    content = resume.content_json
    if resume.ai_enhanced:
        # Assume content has sections like jobs, projects
        for section in ["jobs", "projects"]:
            if section in content:
                for item in content[section]:
                    if "description" in item:
                        item["description"] = await AIService.enhance_text(item["description"], f"in {section} section")

    db_resume = Resume(**resume.dict(), user_id=current_user.id)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

@router.get("/", response_model=list[ResumeResponse])
def get_resumes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Resume).filter(Resume.user_id == current_user.id).all()

@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(resume_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(resume_id: uuid.UUID, resume_update: ResumeUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    for key, value in resume_update.dict(exclude_unset=True).items():
        setattr(resume, key, value)

    if resume_update.ai_enhanced and resume_update.content_json:
        content = resume_update.content_json
        for section in ["jobs", "projects"]:
            if section in content:
                for item in content[section]:
                    if "description" in item:
                        item["description"] = await AIService.enhance_text(item["description"], f"in {section} section")

    db.commit()
    db.refresh(resume)
    return resume

@router.delete("/{resume_id}")
def delete_resume(resume_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted"}

@router.post("/{resume_id}/generate-pdf")
async def generate_pdf(resume_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    template = db.query(Template).filter(Template.id == resume.template_id).first()
    latex_content = LaTeXService.render_template(template.content, resume.content_json)
    output_path = f"resumes/{resume_id}.pdf"
    success = LaTeXService.generate_pdf(latex_content, output_path)
    if success:
        return {"pdf_url": output_path}
    else:
        raise HTTPException(status_code=500, detail="PDF generation failed")
