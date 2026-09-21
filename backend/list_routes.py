import glob, re
endpoints = []
for file in glob.glob('src/api/*.py'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'@router\.(get|post|put|patch|delete)\("([^"]+)"', content)
    for method, path in matches:
        # Resolve prefixes if possible. Hardcoded based on main.py imports:
        # auth: /api/v1/auth
        # student: /api/v1/students
        # recruiter: /api/v1/recruiters (actually recruiter.py doesn't have prefix in include_router, let's assume it mounts as is?) Wait, in main.py recruiter is included without prefix, so its paths in the file are already full, or maybe it mounts on /
        # Actually in main.py: app.include_router(recruiter_router) -> no prefix.
        if file.endswith('auth.py') and not path.startswith('/api/v1'):
            path = '/api/v1/auth' + path
        elif file.endswith('student.py') and not path.startswith('/api/v1'):
            path = '/api/v1/students' + path
        elif file.endswith('readiness.py') and not path.startswith('/api/v1'):
            path = '/api/v1/readiness' + path
        endpoints.append(f"{method.upper()} {path}")

endpoints.sort()
print(f"Total endpoints: {len(endpoints)}")
for e in endpoints:
    print(e)
