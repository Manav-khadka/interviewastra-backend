from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from app.modules.auth.routes import router as auth_router
from app.modules.resumes.routes import router as resumes_router
from app.modules.analysis.routes import router as analysis_router
from app.modules.job_prep.routes import router as job_prep_router
from app.db.init_db import init_db, seed_db
from app.middlewares.logging import LoggingMiddleware
from app.core.logging import logger
from app.core.config import settings

init_db()
seed_db()

# Configure FastAPI with custom Swagger UI
app = FastAPI(
    title="InterviewAstra API",
    description=f"""
    🚀 **InterviewAstra Backend API**
    
    {"🧪 **TESTING MODE ENABLED** - Authentication is bypassed!" if settings.testing_mode else "🔒 **Production Mode** - Authentication required"}
    
    ### Testing Credentials (for manual login if needed):
    - **Username**: manav@test.com
    - **Password**: manav123
    
    ### Quick Start:
    1. All protected endpoints automatically use the test user "Manav" in testing mode
    2. No need to authenticate manually in Swagger!
    3. Just click "Try it out" and execute any endpoint
    
    {"⚠️ **Note**: Set `TESTING_MODE=false` in .env for production" if settings.testing_mode else ""}
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(LoggingMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(resumes_router, prefix="/resumes", tags=["resumes"])
app.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
app.include_router(job_prep_router, prefix="/job-prep", tags=["job-prep"])

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {
        "API": "InterviewAstra is running successfully v1.0",
        "testing_mode": settings.testing_mode,
        "default_user": settings.default_test_user_name if settings.testing_mode else None,
        "message": "Authentication bypassed in testing mode" if settings.testing_mode else "Authentication required"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "testing_mode": settings.testing_mode
    }