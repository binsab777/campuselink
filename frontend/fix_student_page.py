with open('src/app/dashboard/students/page.tsx', 'r') as f: c = f.read()
c = c.replace('href={`http://localhost:8000${s.resume_url}`}', 'href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001"}${s.resume_url.replace("/api/v1", "")}`}')
with open('src/app/dashboard/students/page.tsx', 'w') as f: f.write(c)
