# Laravel Architecture

## Design Principles
- **API First**: The backend exclusively provides JSON endpoints formatted via API Resources.
- **Form Requests**: All incoming data is validated strictly using Laravel Form Requests before hitting Controllers.
- **Service Layer**: Business logic (especially Phase 6 scoring) is extracted to dedicated Service classes (`ReadinessScoringService`, `SkillGapService`, `EligibilityService`).
- **Strict Typing**: PHP 8.3+ strong typing used throughout models and services.
- **Resource Ownership**: Enforced heavily through Laravel Policies (`StudentPolicy`, `JobPolicy`).

## Key Components
- **Controllers**: Thin wrappers translating HTTP logic to Service logic.
- **Enums**: Used extensively mapping FastAPI enums to PHP 8.1+ Enums.
- **Seeders**: Configured to rebuild exact state for deterministic AI/Readiness testing.
