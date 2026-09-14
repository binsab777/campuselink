from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import verify_password, hash_password, create_access_token, create_refresh_token, decode_token
from src.models.all_models import User
from src.schemas.auth import Token, UserCreate, UserOut
from src.api.dependencies import get_current_user
from src.models.enums import UserRole

router = APIRouter()

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # We use OAuth2PasswordRequestForm which expects 'username' and 'password'
    # We treat 'username' as 'email'
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token = create_access_token(subject=user.id, role=user.role.value)
    refresh_token = create_refresh_token(subject=user.id, role=user.role.value)
    
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

from src.models.all_models import User, Student, Recruiter, Company
import datetime

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if user_in.role == UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Cannot register as SUPER_ADMIN")
    if user_in.role in [UserRole.PLACEMENT_OFFICER, UserRole.MENTOR]:
        raise HTTPException(status_code=403, detail=f"Cannot register as {user_in.role.value}")
    
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = hash_password(user_in.password)
    new_user = User(
        email=user_in.email,
        password_hash=hashed_password,
        role=user_in.role
    )
    db.add(new_user)
    db.flush()

    if user_in.role == UserRole.STUDENT:
        name_prefix = user_in.email.split("@")[0]
        student = Student(
            user_id=new_user.id,
            student_identifier=f"STU{new_user.id:04d}",
            first_name=name_prefix.capitalize(),
            last_name="Student",
            branch="Computer Science",
            graduation_year=datetime.datetime.now().year + 2,
            cgpa=8.0,
            backlogs_current=0,
            backlogs_history=0,
        )
        db.add(student)
    elif user_in.role == UserRole.RECRUITER:
        company_name = f"{user_in.email.split('@')[0].capitalize()} Technologies"
        company = Company(
            name=company_name,
            industry="Information Technology",
            size="51-200"
        )
        db.add(company)
        db.flush()
        recruiter = Recruiter(
            user_id=new_user.id,
            company_id=company.id,
            contact_name=user_in.email.split("@")[0].capitalize(),
            contact_email=user_in.email
        )
        db.add(recruiter)

    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
            
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")
            
        access_token = create_access_token(subject=user.id, role=user.role.value)
        new_refresh_token = create_refresh_token(subject=user.id, role=user.role.value)
        
        return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
