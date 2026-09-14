# CAMPUSLINK

An AI-Powered Campus-to-Corporate Placement Management & Analytics Platform.
This platform bridges the gap between students, recruiters, and placement officers by offering comprehensive profiles, job postings, deterministic readiness scoring, and skill-gap analysis.

## Features Currently Implemented (Phases 1-6)
- **Role-Based Workflows**: Tailored portals for Students, Recruiters, Placement Officers, and Super Admins.
- **Student Profiles**: End-to-end management of academic history, projects, verified skills, and resumes.
- **Corporate & Job Management**: Recruiter dashboard to post jobs, manage company profiles, and track applicants.
- **Placement Drives**: Orchestrate placement drives and bulk-register candidates.
- **Student Readiness Engine**: Evaluates a student profile across 7 core employability pillars (Academic, Technical, Projects, Certifications, etc.) and calculates a deterministic readiness score (e.g. 'DEVELOPING', 'READY').
- **Skill-Gap Analysis**: Job-specific skill gap analysis comparing a student's verified skills against a job's requirements.

## Tech Stack
- **Frontend**: Next.js 14, React, Tailwind CSS, TypeScript
- **Backend**: FastAPI, Python 3.10+, SQLAlchemy, Pydantic, Alembic
- **Database**: SQLite (default for local testing), PostgreSQL (Production ready)

---

## Local Development Setup Guide

Follow these instructions to set up the project locally on your system.

### Prerequisites
- [Node.js](https://nodejs.org/en/) (v18+ recommended)
- [Python](https://www.python.org/downloads/) (v3.10+ recommended)
- [Git](https://git-scm.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/binsab777/campuselink.git
cd campuslink
```

### 2. Backend Setup
The backend is built with FastAPI.

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```
2. **Create a Python Virtual Environment**:
   ```bash
   # Windows
   python -m venv venv
   
   # macOS/Linux
   python3 -m venv venv
   ```
3. **Activate the Virtual Environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Set up Environment Variables**:
   Create a `.env` file in the `backend` directory (optional for SQLite, but recommended):
   ```env
   AUTH_JWT_SECRET="your-super-secret-key"
   AUTH_JWT_ALGORITHM="HS256"
   # To use Postgres instead of default SQLite, add:
   # DATABASE_URL="postgresql://user:password@localhost:5432/campuslink_db"
   ```
6. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```
7. **Start the Backend Server**:
   ```bash
   fastapi dev src/main.py
   # Or alternatively: python -m uvicorn src.main:app --reload --port 8000
   ```
   *The API will be available at `http://localhost:8000`. You can access the automatic interactive API documentation at `http://localhost:8000/docs`.*

### 3. Frontend Setup
The frontend is built with Next.js App Router.

1. **Open a new terminal and navigate to the frontend directory** (from the root of the project):
   ```bash
   cd frontend
   ```
2. **Install Node Dependencies**:
   ```bash
   npm install
   ```
3. **Configure Environment Variables**:
   Create a `.env.local` file in the `frontend` directory:
   ```env
   NEXT_PUBLIC_API_URL="http://localhost:8000"
   ```
4. **Start the Frontend Development Server**:
   ```bash
   npm run dev
   ```
   *The web application will be available at `http://localhost:3000`.*

---

## Accessing the Application

Once both servers are running:
1. Open your browser and go to `http://localhost:3000`
2. You can register as a `STUDENT` or `RECRUITER` from the UI.
3. *Note: `SUPER_ADMIN` or `PLACEMENT_OFFICER` accounts currently must be assigned via database manipulation or by an existing admin.*

### Running Backend Tests
Ensure your virtual environment is active, then run:
```bash
cd backend
python -m pytest tests/
```
