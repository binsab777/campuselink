# AI/ML Architecture

## 1. Goal
Provide explainable, transparent AI recommendations for student-job matching, skill-gap analysis, and overall readiness. Avoid black-box decisions; users must understand *why* a match was made.

## 2. Core Flow: Match Generation

1. **Text Extraction**:
   - **Resume**: Extract raw text from PDF/Word using `pdfminer` or similar.
   - **Job Description (JD)**: Raw text from recruiter input.
2. **Skill Extraction (NER / Parsing)**:
   - Use NLP (e.g., `spacy` or an LLM prompt) to extract specific entities (Programming Languages, Frameworks, Soft Skills) from the raw text.
   - Map extracted text to the Master `skills` table to normalize terminology (e.g., "React.js" and "React" -> "React").
3. **Embeddings Generation**:
   - Use `sentence-transformers` (e.g., `all-MiniLM-L6-v2`) to generate dense vector embeddings of the normalized skill sets and project descriptions.
4. **Vector Storage**:
   - Store vectors in PostgreSQL using `pgvector`.
5. **Matching Engine (Similarity Search)**:
   - Calculate Cosine Similarity between a Student's Profile Vector and a Job's Requirement Vector.
6. **Scoring & Explainability**:
   - Combine Vector Similarity Score with Rule-based Filtering (e.g., CGPA cutoff, branch eligibility).
   - Generate "Explainable Reasons":
     - *Positive*: "Matches 4/5 required skills: Python, React, SQL, AWS."
     - *Negative*: "Missing mandatory skill: Docker."
7. **Delivery**:
   - Save matching scores and JSON reasons in `matching_scores` and `skill_gaps` tables.

## 3. Explainable Recommendation Structure
Instead of just returning a score (e.g., `85%`), the API returns:
```json
{
  "score": 85,
  "matched_skills": ["Python", "FastAPI"],
  "missing_skills": ["Docker"],
  "explanation": "Strong match on backend frameworks, but lacks required containerization experience."
}
```

## 4. RAG / AI Assistant (Future)
- A conversational interface for Placement Officers to ask questions like: *"Which students are best suited for the upcoming Amazon drive?"*
- Uses Retrieval-Augmented Generation (RAG): Queries the DB for top students, then passes the structured data to an LLM to formulate a natural language response.
