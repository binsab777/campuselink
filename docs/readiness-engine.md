# CAMPUSLINK — Student Readiness & Skill-Gap Engine

## 1. Overview
The **Student Readiness & Skill-Gap Engine** is a deterministic, explainable service layer built to evaluate a student's employability and benchmark their preparation against specific job descriptions.

### Core Distinctions
- **Profile Completeness (Phase 4):** Measures how many required profile fields have been entered (e.g., 85% data completeness).
- **Hard Eligibility (Phase 5):** Evaluates deterministic binary criteria (e.g., CGPA >= 7.5, zero backlogs, allowed branch).
- **Global Readiness (Phase 6):** Evaluates multidimensional, weighted employability baseline (0–100) independent of any single job.
- **Skill Gap (Phase 6):** Identifies the discrete delta between a student's capabilities and a target job's skill requirements.
- **Job-Specific Readiness (Phase 6):** Evaluates tailored alignment (0–100%) against a specific job role.
- **AI Match Score (Phase 7 - Future):** Hybrid semantic embeddings and ranking model comparing candidate profiles with job embeddings.

---

## 2. Global Readiness Scoring Methodology

### A. Component Weights (`v1.0`)
Readiness is computed across seven transparent dimensions:

| Dimension | Configured Weight | Description |
| :--- | :---: | :--- |
| **Technical Skills** | **30%** | Proficiency levels across registered technical skills, depth, and verified sources |
| **Academic Performance** | **20%** | CGPA normalized out of 10.0 with deductions for active and historical backlogs |
| **Project Portfolio** | **15%** | Quantity, documentation depth, technologies used, and public repository links |
| **Certifications** | **10%** | Verified industry certifications and credential validity |
| **Aptitude & Cognitive Tests** | **10%** | Performance in standardized aptitude, coding, and cognitive assessments |
| **Communication & Soft Skills** | **10%** | Verbal communication assessments and soft skills proficiency |
| **Mock Interview Performance** | **5%** | Performance in simulated technical/HR interviews |
| **Total** | **100%** | |

### B. Normalization Rules (0–100 Scale)
1. **Academic Performance:**
   $$\text{Base} = \min\left(100.0, \frac{\text{CGPA}}{10.0} \times 100\right)$$
   $$\text{Penalty} = (\text{active\_backlogs} \times 15.0) + (\text{historical\_backlogs} \times 5.0)$$
   $$\text{Academic Score} = \max(0.0, \min(100.0, \text{Base} - \text{Penalty}))$$

2. **Technical Skills:**
   - Numerical proficiency weights: `BEGINNER = 25.0`, `INTERMEDIATE = 50.0`, `ADVANCED = 75.0`, `EXPERT = 100.0`.
   - Verified source bonus: `+10.0` points if skill is verified via assessment or certification.
   - Breadth factor: $\text{Breadth} = \min(1.0, 0.45 + 0.15 \times N_{\text{skills}})$.
   - $\text{Technical Score} = \text{Average Skill Score} \times \text{Breadth}$.

3. **Project Portfolio:**
   - Base existence: 20 points per project.
   - Description depth (>20 chars): +7 points.
   - Listed tech stack: +5 points.
   - Repository / live URL: +5 points.
   - Clamped to $[0, 100]$.

4. **Certifications:**
   - Verified issuing organization: +15 points.
   - Credential ID: +15 points.
   - Clamped to $[0, 100]$.

5. **Assessments & Soft Skills:**
   - $\text{Score} = \left(\frac{\text{score}}{\text{max\_score}}\right) \times 100$.

### C. Readiness Levels
| Score Range | Readiness Level | Placement Status |
| :---: | :---: | :--- |
| **80.0 – 100.0** | `HIGHLY_EMPLOYABLE` | Priority recommendation for tier-1 placement drives |
| **60.0 – 79.9** | `READY` | Eligible and prepared for standard placement drives |
| **40.0 – 59.9** | `DEVELOPING` | Foundational preparation; requires targeted skill polish |
| **0.0 – 39.9** | `NOT_READY` | Significant foundational gaps; focus on remedial coursework |

---

## 3. Explainable Missing-Data Strategy
When an institutional assessment (such as Mock Interview or Aptitude) has not yet been administered by the college placement cell:
1. **No Silent Zeroes:** Missing institutional components are not zeroed out, preventing arbitrary score drops.
2. **Dynamic Weight Re-Normalization:** The engine dynamically scales the active weights across the available dimensions:
   $$W'_i = \frac{W_i}{\sum_{j \in \text{available}} W_j}$$
3. **Transparent Quality Tracking:** The payload returns `data_quality`:
   - `available_dimensions`: List of verified dimensions.
   - `missing_dimensions`: Dimensions awaiting college evaluation.
   - `completeness_ratio`: Ratio of evaluated dimensions.
   - `weights_redistributed`: Boolean flag indicating proportional adjustment.
4. **Student-Controlled Sections:** For student-controlled inputs (Projects, Certifications, Skills), a count of zero represents an actual gap and is evaluated as 0 with a corresponding weakness recommendation.

---

## 4. Job-Specific Skill-Gap Engine

### A. Proficiency Comparison Hierarchy
Proficiencies are mapped to an ordinal scale:
$$\text{BEGINNER (1)} < \text{INTERMEDIATE (2)} < \text{ADVANCED (3)} < \text{EXPERT (4)}$$

### B. Gap Severity Logic
For each job requirement ($R$) and student skill ($S$):
- If student possesses the skill and $S_{\text{level}} \ge R_{\text{level}}$:
  - **Status:** `MATCHED`
  - **Severity:** `NONE`
- If student possesses the skill but $S_{\text{level}} < R_{\text{level}}$:
  - **Status:** `PARTIAL`
  - $\Delta = R_{\text{level}} - S_{\text{level}}$
  - $\Delta = 1$: `LOW` (Preferred) / `MEDIUM` (Required)
  - $\Delta = 2$: `MEDIUM` (Preferred) / `HIGH` (Required)
  - $\Delta \ge 3$: `HIGH` (Preferred) / `CRITICAL` (Required)
- If student does not possess the skill:
  - **Status:** `MISSING`
  - If **Required** (`is_mandatory=True`):
    - Level 3–4: `CRITICAL`
    - Level 2: `HIGH`
    - Level 1: `MEDIUM`
  - If **Preferred** (`is_mandatory=False`):
    - Level 3–4: `HIGH`
    - Level 2: `MEDIUM`
    - Level 1: `LOW`

### C. Job-Specific Readiness Score
$$\text{Job Readiness} = (S_{\text{mandatory}} \times 0.60) + (S_{\text{preferred}} \times 0.20) + (S_{\text{global}} \times 0.20)$$

---

## 5. Persistence Architecture
- **Historical Readiness Records:** Stored in `student_scores` with `score_type = "READINESS"`, preserving the full calculation history across versions (`model_version = "v1.0"`).
- **Structured Skill Gaps:** Stored in `skill_gaps` with `(student_id, job_id, skill_id)` unique constraint, maintaining `gap_severity`, `current_level`, `required_level`, `is_mandatory`, and `recommendation`.

---

## 6. API Endpoints
- `GET /api/v1/readiness/me`: Get latest readiness evaluation.
- `POST /api/v1/readiness/me/recalculate`: Trigger fresh calculation and persist new record.
- `GET /api/v1/readiness/me/jobs/{job_id}/skill-gaps`: Get skill gap breakdown against a target job.
- `POST /api/v1/readiness/me/jobs/{job_id}/skill-gaps/analyze`: Force re-evaluation against a target job.
- `GET /api/v1/readiness/students/{student_id}`: Admin/PO review endpoint.
- `GET /api/v1/readiness/students/{student_id}/jobs/{job_id}/skill-gaps`: Admin/PO review endpoint.
