from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.session import get_db
from app.modules.auth.models import User, AuthProviderEnum, UserRole
from app.modules.auth.schemas import UserCreate, UserResponse, OAuthUserCreate
from app.core.security import verify_password, get_password_hash, create_access_token
from typing import Optional

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, identifier: str, password: str):
    """
    Authenticate user by email or username
    identifier can be either email or username
    """
    # Try to find user by email or username
    user = db.query(User).filter(
        or_(User.email == identifier, User.username == identifier)
    ).first()
    
    if not user:
        return False
    
    # Check if user has a password (email auth users)
    if not user.password:
        return False
        
    if not verify_password(password, user.password):
        return False
    
    return user

def get_or_create_oauth_user(
    db: Session, 
    email: str, 
    name: str, 
    provider: AuthProviderEnum, 
    provider_id: str,
    username: Optional[str] = None
) -> User:
    """
    Get existing OAuth user or create a new one
    """
    # Check if user exists with this provider_id
    user = db.query(User).filter(
        User.provider_id == provider_id,
        User.auth_provider == provider
    ).first()
    
    if user:
        return user
    
    # Check if user exists with this email (might be switching auth providers)
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Update existing user to add OAuth provider
        user.auth_provider = provider
        user.provider_id = provider_id
        db.commit()
        db.refresh(user)
        return user
    
    # Create new OAuth user
    # Generate unique username if not provided
    if not username:
        username = email.split('@')[0]
        # Ensure username is unique
        base_username = username
        counter = 1
        while db.query(User).filter(User.username == username).first():
            username = f"{base_username}{counter}"
            counter += 1
    
    user = User(
        username=username,
        name=name,
        email=email,
        password=None,  # No password for OAuth users
        auth_provider=provider,
        provider_id=provider_id,
        role=UserRole.user
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    
    # Create user with explicit enum values
    db_user = User(
        username=user.email,
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=UserRole.user,
        auth_provider=AuthProviderEnum.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login with email or username and password
    OAuth2 compatible endpoint for Swagger UI
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id)})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "username": user.username
        }
    }

@router.post("/google", response_model=dict)
def google_login(oauth_user: OAuthUserCreate, db: Session = Depends(get_db)):
    """
    Login or register with Google OAuth
    Frontend should send the Google user data after OAuth flow
    """
    user = get_or_create_oauth_user(
        db=db,
        email=oauth_user.email,
        name=oauth_user.name,
        provider=AuthProviderEnum.google,
        provider_id=oauth_user.provider_id,
        username=oauth_user.username
    )
    
    access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "username": user.username,
            "auth_provider": user.auth_provider.value
        }
    }

@router.post("/github", response_model=dict)
def github_login(oauth_user: OAuthUserCreate, db: Session = Depends(get_db)):
    """
    Login or register with GitHub OAuth
    Frontend should send the GitHub user data after OAuth flow
    """
    user = get_or_create_oauth_user(
        db=db,
        email=oauth_user.email,
        name=oauth_user.name,
        provider=AuthProviderEnum.github,
        provider_id=oauth_user.provider_id,
        username=oauth_user.username
    )
    
    access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "username": user.username,
            "auth_provider": user.auth_provider.value
        }
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(db: Session = Depends(get_db)):
    """
    Get current authenticated user information
    """
    from app.core.dependencies import get_current_user
    user = get_current_user(db=db)
    return user