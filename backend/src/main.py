from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth import router as auth_router
from src.models.enums import UserRole
from src.api.dependencies import require_role
from src.models.all_models import User

from src.api.student import router as student_router
from src.api.recruiter import router as recruiter_router
from src.api.recruiter import jobs_router, drives_router
from src.api.readiness import router as readiness_router
from src.api.admin import router as admin_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="CAMPUSLINK API", version="1.0.0")

# Ensure uploads directory exists
os.makedirs("./uploads/resumes", exist_ok=True)
app.mount("/static/resumes", StaticFiles(directory="./uploads/resumes"), name="resumes")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(student_router, prefix="/api/v1/students", tags=["Student Profile"])
app.include_router(recruiter_router)
app.include_router(jobs_router)
app.include_router(drives_router)
app.include_router(readiness_router)
app.include_router(admin_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/v1/admin/only", dependencies=[Depends(require_role(UserRole.SUPER_ADMIN))])
def admin_only(current_user: User = Depends(require_role(UserRole.SUPER_ADMIN))):
    return {"message": "Welcome Admin"}
