# CAMPUSLINK Architecture

## 1. Overview
CAMPUSLINK is an AI-powered Campus-to-Corporate Placement Management & Analytics Platform. It is designed as a **Modular Monolith** to ensure rapid development, easier deployment, and straightforward debugging, with the flexibility to scale out into microservices in the future if required.

## 2. Technology Stack

### Frontend
- **Framework**: Next.js (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Component Library**: shadcn/ui
- **State Management**: React Context / Zustand / React Query

### Backend
- **Framework**: FastAPI (Python)
- **Language**: Python 3.11+
- **Data Validation**: Pydantic v2
- **ORM**: SQLAlchemy 2.0
- **Database Migrations**: Alembic

### Database
- **Primary Database**: PostgreSQL 15+
- **Vector Extension**: `pgvector` for storing embeddings (Skills, Resumes, JDs).

### AI & ML Ecosystem
- **Libraries**: `scikit-learn`, `sentence-transformers`, `spacy`
- **Search**: Vector similarity search in PostgreSQL via `pgvector`.
- **LLM Integration**: LangChain or direct API calls for explainable AI summaries and RAG.

### Infrastructure & Background Processing
- **Containerization**: Docker & Docker Compose
- **Caching & Broker**: Redis
- **Background Jobs**: Celery (or RQ/Arq) for heavy tasks (email, embedding generation, report generation).

## 3. Recommended Folder Structure

```
campuslink/
├── frontend/                # Next.js Application
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # Reusable UI components
│   │   ├── lib/             # API clients, utils
│   │   ├── hooks/           # Custom React hooks
│   │   └── types/           # TypeScript definitions
│   └── package.json
├── backend/                 # FastAPI Application
│   ├── src/
│   │   ├── api/             # API Routers (v1)
│   │   ├── core/            # Config, Security, DB session
│   │   ├── models/          # SQLAlchemy Models
│   │   ├── schemas/         # Pydantic Schemas
│   │   ├── services/        # Business Logic
│   │   ├── tasks/           # Background/Celery tasks
│   │   └── ml/              # AI/ML logic, embeddings extraction
│   ├── tests/               # Pytest tests
│   ├── alembic/             # Database migrations
│   └── requirements.txt
├── docs/                    # Project Documentation
├── datasets/                # Sample data, ML training artifacts (ignored in git)
├── docker-compose.yml       # Infrastructure orchestration
└── README.md
```

## 4. Architectural Principles
- **Separation of Concerns**: API routing, business logic, and database access are strictly separated.
- **Explainability over Black-box**: AI outputs and deterministic evaluations (readiness, skill gaps) must have traceable reasons and granular breakdowns.
- **Asynchronous Processing**: Heavy AI tasks (resume parsing, matching calculations) occur in background queues, not in the main request-response cycle.
- **Strong Typing**: Pydantic schemas enforce strict data contracts between frontend and backend.

## 5. Evaluation Layer Hierarchy (Phase 6)
CAMPUSLINK strictly demarcates evaluation phases:
1. **Profile Completeness (Phase 4):** Measures field completion.
2. **Deterministic Hard Eligibility (Phase 5):** Binary qualification rules (CGPA, backlogs, branch).
3. **Global Readiness Engine (Phase 6):** Weighted multidimensional baseline score (0–100) across Academics, Technical Skills, Projects, Certifications, Assessments, Communication, and Interview.
4. **Job-Specific Skill-Gap Engine (Phase 6):** Structured comparison against job requirements with ordinal proficiency deltas (1–4), severity categorization (NONE, LOW, MEDIUM, HIGH, CRITICAL), and actionable domain-grounded recommendations.
5. **AI Semantic Matching (Phase 7 - Future):** Vector embeddings, hybrid ranking, and neural re-ranking.

