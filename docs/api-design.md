# API Design (RESTful)

The backend follows RESTful principles using FastAPI. All endpoints are prefixed with `/api/v1`.

## Authentication & Users
- `POST /auth/login` - Authenticate and return JWT.
- `POST /auth/register` - Register new user.
- `GET /users/me` - Get current user profile.

## Students
- `GET /students` - List students (Placement Officer / Admin).
- `GET /students/{id}` - Get student details.
- `PUT /students/{id}` - Update student profile.
- `GET /students/{id}/skills` - Get student skills.
- `POST /students/{id}/resume` - Upload and parse resume.

## Recruiters
- `GET /recruiters` - List companies.
- `POST /recruiters` - Create company profile.
- `GET /recruiters/{id}` - Get company details.

## Jobs
- `GET /jobs` - List jobs (Filterable by status, company).
- `POST /jobs` - Create a new job posting.
- `GET /jobs/{id}` - Get job details.

## Applications
- `GET /applications` - List applications.
- `POST /applications` - Apply for a job.
- `PATCH /applications/{id}/status` - Update application status.

## Placement Drives
- `GET /drives` - List placement drives.
- `POST /drives` - Create a drive.
- `POST /drives/{id}/students` - Add students to drive.

## Interviews
- `GET /interviews` - List interviews.
- `POST /interviews` - Schedule an interview.
- `PATCH /interviews/{id}` - Update interview status/feedback.

## Offers
- `GET /offers` - List offers.
- `POST /offers` - Roll out an offer.
- `POST /offers/{id}/documents` - Upload offer document.

## Analytics
- `GET /analytics/dashboard` - Get high-level stats (Admin/PO).
- `GET /analytics/skills` - Get skill demand trends.

## AI & Matching
- `GET /ai/match/student/{student_id}/jobs` - Recommend jobs for a student.
- `GET /ai/match/job/{job_id}/students` - Recommend students for a job.
- `GET /ai/skill-gap/student/{student_id}/job/{job_id}` - Analyze skill gap.
- `POST /ai/parse-jd` - Extract structured requirements from raw JD text.
