# Database initialization and seeding
from app.db.session import engine, Base
# Import all models to ensure they are registered with Base
from app.modules.auth.models import User, UserRole, AuthProviderEnum
from app.modules.resumes.models import Resume
from app.modules.template.models import Template
from app.modules.analysis.models import ResumeAnalysis
from app.modules.job_prep.models import JobDescription, JobPrepKit
from app.core.security import get_password_hash
from app.core.config import settings

def init_db():
    Base.metadata.create_all(bind=engine)

def seed_db():
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        # Create default test user "manav" for easy testing
        test_user = db.query(User).filter(User.email == settings.default_test_user_email).first()
        if not test_user:
            hashed_password = get_password_hash(settings.default_test_user_password)
            test_user = User(
                username="manav",
                name=settings.default_test_user_name,
                email=settings.default_test_user_email,
                password=hashed_password,
                role=UserRole.admin,  # Give admin role for testing
                auth_provider=AuthProviderEnum.email
            )
            db.add(test_user)
            print(f"✓ Created default test user: {settings.default_test_user_name} ({settings.default_test_user_email})")
            print(f"  Username: manav")
            print(f"  Password: {settings.default_test_user_password}")
        
        # Keep the original user if you want
        original_user = db.query(User).filter(User.email == "manavkhadka2004@gmail.com").first()
        if not original_user:
            hashed_password = get_password_hash("#Manav@423")
            original_user = User(
                username="manavkhadka2004@gmail.com",
                name="manav khadka",
                email="manavkhadka2004@gmail.com",
                password=hashed_password,
                role=UserRole.admin,
                auth_provider=AuthProviderEnum.email
            )
            db.add(original_user)
        
        db.commit()
    except Exception as e:
        print(f"⚠️  Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()