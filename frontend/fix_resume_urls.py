import re

def fix_links(path):
    with open(path, 'r') as f:
        c = f.read()
    
    # Replace `http://localhost:8000${...}` with `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}${...}`
    c = c.replace('href={`http://localhost:8000${resumeUrl}`}', 'href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001"}${resumeUrl.replace("/api/v1", "")}`}')
    c = c.replace('href={`http://localhost:8000${profile.resume_url}`}', 'href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001"}${profile.resume_url.replace("/api/v1", "")}`}')
    
    with open(path, 'w') as f:
        f.write(c)

fix_links('src/features/students/ResumeCard.tsx')
fix_links('src/features/recruiters/CandidateProfileModal.tsx')
