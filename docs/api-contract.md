# API Contract

The Laravel API perfectly mirrors the legacy FastAPI contract.

## Error Handling
- `401 Unauthenticated`: Missing or invalid Sanctum token.
- `403 Forbidden`: Role check (`CheckRole` middleware) or Policy ownership check failed.
- `404 Not Found`: Eloquent `findOrFail()` bound exceptions.
- `422 Unprocessable Entity`: Form Request validation failures. Maps exactly to the frontend's field error normalization.
- `500 Server Error`: Unhandled exceptions.

## Common Responses
### 1. Readiness Scoring
Endpoint: `POST /api/v1/students/me/recalculate`
Returns:
```json
{
  "version": "v1.0",
  "overall_score": 85.5,
  "readiness_level": "HIGHLY_EMPLOYABLE",
  "dimensions": {
    "academic": 90.0,
    ...
  }
}
```

### 2. Skill Gaps
Endpoint: `GET /api/v1/jobs/{job}/skill-gaps`
Returns Array of:
```json
{
  "skill_id": 1,
  "gap_severity": "CRITICAL",
  "current_level": 1,
  "required_level": 4,
  ...
}
```
